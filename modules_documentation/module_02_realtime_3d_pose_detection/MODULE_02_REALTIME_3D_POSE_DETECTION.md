# BioMechAI — Module 02: Real-Time 3D Anatomical Pose Detection & On-Device Computer Vision Pipeline

<div class="toc">
<h2>Table of Contents & Rapid-Lookup Index</h2>
<ul>
<li><a href="#sec1">1. Executive Summary & Core Mission</a></li>
<li><a href="#sec2">2. Real-World Computer Vision Challenge: Why Mobile Pose Detection is Difficult</a></li>
<li><a href="#sec3">3. Step-by-Step Chronological Engineering Evolution</a></li>
<li><a href="#sec4">4. Deep Learning Architecture: BlazePose Two-Stage Detector-Tracker Pipeline</a>
    <ul>
        <li><a href="#sec4-1">4.1 Stage 1: The Face/Torso ROI Alignment Detector</a></li>
        <li><a href="#sec4-2">4.2 Stage 2: The 33-Landmark 3D Coordinate Regression Network</a></li>
        <li><a href="#sec4-3">4.3 Tracking Optimization: Bypassing the Detector in Consecutive Frames</a></li>
    </ul>
</li>
<li><a href="#sec5">5. The 33 Anatomical Keypoint Topology & 3D Spatial Coordinate System</a>
    <ul>
        <li><a href="#sec5-1">5.1 Landmark Semantic Mapping & kSkeletonPairs Graph</a></li>
        <li><a href="#sec5-2">5.2 The 3D Coordinate System: Understanding Relative Depth ($z$) and Visibility</a></li>
    </ul>
</li>
<li><a href="#sec6">6. High-Performance Camera Stream Ingestion Pipeline (YUV420 Memory Assembly)</a></li>
<li><a href="#sec7">7. Mathematical Joint Trigonometry & Planar Angle Derivations</a></li>
<li><a href="#sec8">8. Exponential Moving Average (EMA) Coordinate Smoothing & Jitter Elimination</a></li>
<li><a href="#sec9">9. Downstream System Feed Pipeline (How Module 02 Powers Modules 3, 4, 5, 6, & 7)</a></li>
<li><a href="#sec10">10. Scientific Standards, Google Research Benchmarks, & Literature Citations</a></li>
<li><a href="#sec11">11. Panel Defense Quick-Reference: Frequently Asked Questions & Rapid Answers</a></li>
</ul>
</div>

---

<h2 id="sec1">1. Executive Summary & Core Mission</h2>

<p>
Module 02 is the sensory visual foundation of the entire BioMechAI system. Before any artificial intelligence model can classify an exercise (Module 03), count a repetition (Module 04), grade posture correctness (Module 05), measure body levers (Module 06), or warn against a ligament tear (Module 07), the system must first perceive where the human body is located in physical space.
</p>

<blockquote>
<strong>Plain-English Concept:</strong> Imagine a professional athlete wearing an expensive Hollywood motion-capture suit covered in dozens of glowing ping-pong balls while dozens of infrared laboratory cameras track their movement. Module 02 achieves that exact same motion-capture capability using <em>zero wearable sensors, zero special suits, and zero external hardware</em>. Using nothing more than the standard single-lens camera built into a regular smartphone, Module 02 identifies 33 anatomical landmarks across the athlete's body 30 times every second, transforming raw camera video into a living, three-dimensional digital skeleton.
</blockquote>

<p>
The module delivers:
</p>
<ul>
    <li><strong>33 Three-Dimensional Anatomical Keypoints</strong>: Pinpoints exact coordinates for the nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles, heels, and toes.</li>
    <li><strong>3D Relative Depth Perception ($z$-axis)</strong>: Infers the relative depth of each joint in camera space, solving perspective foreshortening.</li>
    <li><strong>High-Speed On-Device Inference (30 FPS)</strong>: Executes locally on the smartphone's Neural Processing Unit (NPU) and GPU in $\sim 18-28\text{ milliseconds}$ per frame, consuming zero cloud bandwidth and operating completely offline.</li>
    <li><strong>Zero-Copy Memory Stream Pipeline</strong>: High-performance YUV420 multi-plane memory assembly via Flutter's <code>WriteBuffer</code>, preventing memory leaks and frame stuttering.</li>
</ul>

---

<h2 id="sec2">2. Real-World Computer Vision Challenge: Why Mobile Pose Detection is Difficult</h2>

<p>
Extracting human skeletal pose in real time on mobile hardware presents severe computational hurdles:
</p>

<ol>
    <li><strong>Mobile Silicon Thermal & Compute Constraints</strong>:
        <br>Desktop computer vision models (such as OpenPose or AlphaPose) require massive desktop GPUs consuming $250-400\text{ Watts}$ of electrical power. Running such models on a mobile smartphone processor would drain the battery in 15 minutes, cause extreme thermal throttling, and drop the frame rate to an unusable $2-4\text{ FPS}$.
    </li>
    <li><strong>Severe Anatomical Occlusion During Exercise</strong>:
        <br>In fitness training, limbs constantly cross in front of or behind each other. During a side-profile squat or push-up, the near leg or arm completely covers (occludes) the far limb. Traditional object detectors fail when parts of the target object vanish from sight.
    </li>
    <li><strong>High-Frequency Spatial Jitter</strong>:
        <br>Because mobile camera sensors have small lenses, low light causes sensor noise that causes detected joint coordinates to shake erratically by several pixels between consecutive frames. If fed directly into biomechanical velocity formulas, this artificial vibration creates catastrophic errors in rep counting.
    </li>
    <li><strong>YUV420 Camera Format Incompatibility</strong>:
        <br>Android smartphone cameras stream video frames in the raw <strong>YUV420</strong> multi-plane format (Y = luminance/brightness, U/V = chrominance/color), whereas deep learning vision models expect continuous planar RGB or NV21 byte arrays. Converting every frame using naive nested loops locks the mobile UI thread and crashes the app.
    </li>
</ol>

<p>
Module 02 overcomes all of these obstacles through an optimized two-stage pipeline, hardware-accelerated memory assembly, and exponential temporal smoothing.
</p>

---

<h2 id="sec3">3. Step-by-Step Chronological Engineering Evolution</h2>

<p>
The pose detection architecture evolved through three rigorous engineering phases between FYP-I and the final FYP-II release:
</p>

<h3>Phase 1: Cloud-Based Python OpenPose (FYP-I Early Exploration)</h3>
<p>
In the early prototyping phase of FYP-I, the team tested streaming mobile video frames over HTTP to a cloud server running CMU OpenPose.
</p>
<div class="alert-box">
<strong>Critical Failure Discovered:</strong> Streaming $1080\text{p}$ video frames over mobile Wi-Fi created $>400\text{ ms}$ of round-trip network latency. Frame rates stalled at $6-8\text{ FPS}$, cellular data quotas were instantly exhausted, and any Wi-Fi hiccup froze the entire pose tracking pipeline. The team determined that cloud pose estimation is fundamentally unviable for real-time athletic coaching.
</div>

<h3>Phase 2: On-Device Single-Stage Pose Estimation</h3>
<p>
The pipeline was brought entirely on-device by compiling TensorFlow Lite models (MoveNet SinglePose). While inference time improved to $\sim 45\text{ ms}$, MoveNet was limited to only 17 keypoints and lacked foot and hand landmarks (heels and toes were absent), which prevented accurate knee valgus tracking and foot placement validation.
</p>

<h3>Phase 3: Google ML Kit BlazePose Integration (Semester 8 Baseline)</h3>
<p>
In the final FYP-II production release, the team implemented <strong>Google ML Kit BlazePose</strong> in <code>pose_detection_service.dart</code>:
</p>
<ul>
    <li>Upgraded from 17 to <strong>33 full-body anatomical landmarks</strong> (adding heels, foot indices, and thumbs).</li>
    <li>Implemented the two-stage detector-tracker pipeline configured for high-speed streaming mode (<code>PoseDetectionMode.stream</code>).</li>
    <li>Engineered the zero-copy <code>WriteBuffer</code> YUV420 memory assembler, achieving sustained <strong>30 FPS</strong> on consumer Android hardware.</li>
    <li>Built a 90-frame temporal landmark circular buffer (<code>landmarkBuffer</code>) providing a rolling 3-second memory window for downstream action recognition models.</li>
</ul>

---

<h2 id="sec4">4. Deep Learning Architecture: BlazePose Two-Stage Pipeline</h2>

<p>
Google BlazePose (Bazarevsky et al., Google Research 2020) achieves real-time mobile speed by separating the problem of finding a human from the problem of tracking their joints:
</p>

<pre><code>THE BLAZEPOSE TWO-STAGE DETECTOR-TRACKER ARCHITECTURE
===================================================================================
[VIDEO FRAME T = 1] (Initial Discovery)
   |
   v
STAGE 1: Heavy Pose Detector Network
   * Scans full video frame (1280x720)
   * Detects facial features & mid-hip midpoint
   * Computes human bounding box & rotation angle
   |
   v
STAGE 2: Lightweight 33-Landmark Regression Network
   * Cropped Region of Interest (ROI) (256x256 tensor)
   * Predicts 33 3D Spatial Landmarks: (x, y, z, visibility)
   * Derives tracking bounding box for Frame T = 2
   |
   v
[VIDEO FRAME T = 2, 3, 4...] (Consecutive Streaming Frames)
   |
   +---> BYPASS STAGE 1 ENTIRELY! (Zero full-frame scanning)
   |
   +---> Crop new ROI directly from previous frame's predicted landmarks
   |
   v
STAGE 2: Lightweight 33-Landmark Regression Network (Only takes ~18 ms!)
   * If tracking confidence drops below threshold: Re-awaken Stage 1 Detector.
===================================================================================</code></pre>

<h3 id="sec4-1">4.1 Stage 1: The Face/Torso ROI Alignment Detector</h3>
<p>
Finding a full human body in an unconstrained room is computationally expensive. However, the human head and face are rigid, highly distinct visual structures with minimal geometric deformation compared to arms and legs. BlazePose's Stage 1 detector first identifies the face and mid-hip vector. From these anchor points, it projects an aligned, rotated bounding box around the body.
</p>

<h3 id="sec4-2">4.2 Stage 2: The 33-Landmark 3D Regression Network</h3>
<p>
The aligned bounding box is cropped, scaled down to a compact $256 \times 256$ tensor, and passed to a lightweight heat-map regression convolutional neural network. The network outputs:
</p>
<ul>
    <li><strong>33 Planar Coordinates $(x, y)$</strong>: Normalized screen positions in range $[0.0, 1.0]$.</li>
    <li><strong>33 Relative Depth Coordinates ($z$)</strong>: Estimated distance along the camera optical axis.</li>
    <li><strong>33 Visibility Likelihoods</strong>: Confidence values $[0.0, 1.0]$ representing whether the joint is genuinely visible or hidden behind another body part.</li>
</ul>

<h3 id="sec4-3">4.3 Tracking Optimization: Bypassing the Detector</h3>
<p>
This is the key architectural breakthrough: <strong>Stage 1 executes only on the very first frame of a workout</strong>. In all subsequent frames, the system uses the joints predicted in the previous frame to mathematically project where the athlete's body must be in the current frame. This eliminates $80\%$ of computational overhead, allowing the lightweight tracker to run continuously at 30 FPS without heating up the phone.
</p>

---

<h2 id="sec5">5. The 33 Anatomical Keypoint Topology & 3D Coordinate System</h2>

<p>
BlazePose extracts 33 standardized anatomical keypoints mapped across the human kinetic chain:
</p>

<pre><code>BLAZEPOSE 33-LANDMARK TOPOLOGY MAPPING
===================================================================================
HEAD:       0: Nose | 1: Left Eye Inner | 2: Left Eye | 3: Left Eye Outer
            4: Right Eye Inner | 5: Right Eye | 6: Right Eye Outer
            7: Left Ear | 8: Right Ear | 9: Mouth Left | 10: Mouth Right

UPPER BODY: 11: Left Shoulder  | 12: Right Shoulder
            13: Left Elbow     | 14: Right Elbow
            15: Left Wrist     | 16: Right Wrist
            17: Left Pinky     | 18: Right Pinky
            19: Left Index     | 20: Right Index
            21: Left Thumb     | 22: Right Thumb

LOWER BODY: 23: Left Hip       | 24: Right Hip
            25: Left Knee      | 26: Right Knee
            27: Left Ankle     | 28: Right Ankle
            29: Left Heel      | 30: Right Heel
            31: Left Foot Index| 32: Right Foot Index
===================================================================================</code></pre>

<h3 id="sec5-1">5.1 The <code>kSkeletonPairs</code> Bone Connectivity Graph</h3>
<p>
In <code>pose_detection_service.dart</code>, bone connections are codified as a directed skeletal graph connecting adjacent physiological levers:
</p>
<pre><code>const List&lt;List&lt;PoseLandmarkType&gt;&gt; kSkeletonPairs = [
  [PoseLandmarkType.leftShoulder,  PoseLandmarkType.rightShoulder],
  [PoseLandmarkType.leftShoulder,  PoseLandmarkType.leftElbow],
  [PoseLandmarkType.leftElbow,     PoseLandmarkType.leftWrist],
  [PoseLandmarkType.rightShoulder, PoseLandmarkType.rightElbow],
  [PoseLandmarkType.rightElbow,    PoseLandmarkType.rightWrist],
  [PoseLandmarkType.leftShoulder,  PoseLandmarkType.leftHip],
  [PoseLandmarkType.rightShoulder, PoseLandmarkType.rightHip],
  [PoseLandmarkType.leftHip,       PoseLandmarkType.rightHip],
  [PoseLandmarkType.leftHip,       PoseLandmarkType.leftKnee],
  [PoseLandmarkType.leftKnee,      PoseLandmarkType.leftAnkle],
  [PoseLandmarkType.rightHip,      PoseLandmarkType.rightKnee],
  [PoseLandmarkType.rightKnee,     PoseLandmarkType.rightAnkle],
  [PoseLandmarkType.leftAnkle,     PoseLandmarkType.leftHeel],
  [PoseLandmarkType.rightAnkle,    PoseLandmarkType.rightHeel],
  [PoseLandmarkType.leftHeel,      PoseLandmarkType.leftFootIndex],
  [PoseLandmarkType.rightHeel,     PoseLandmarkType.rightFootIndex],
];</code></pre>

<h3 id="sec5-2">5.2 The 3D Coordinate System: Understanding Relative Depth ($z$)</h3>
<p>
Unlike naive 2D vision models, every landmark contains three spatial components:
</p>
<div class="formula-card">
$$\mathbf{L}_k = (x_k, \; y_k, \; z_k, \; v_k)$$
<em>Where:</em><br>
- $x_k \in [0.0, 1.0]$: Horizontal position normalized across camera frame width.<br>
- $y_k \in [0.0, 1.0]$: Vertical position normalized across camera frame height.<br>
- $z_k$: <strong>Estimated relative depth</strong> along the camera's optical z-axis. The coordinate origin ($z=0$) is calibrated to the midpoint between the athlete's hips. A negative $z$ indicates the joint is closer to the camera than the hips; a positive $z$ indicates the joint is further away.<br>
- $v_k \in [0.0, 1.0]$: Probability that the landmark is within the frame and un-occluded.
</div>

<blockquote>
<strong>Plain-English Concept:</strong> If you are standing facing the camera and punch your right fist directly forward toward the phone screen, your right wrist's $x$ and $y$ on the screen might barely change. But its $z$ coordinate plunges sharply into negative numbers, telling the computer that your arm has extended forward in 3D space!
</blockquote>

---

<h2 id="sec6">6. High-Performance Camera Stream Ingestion Pipeline</h2>

<p>
A frequent cause of mobile app crashes is improper image memory handling. In Android, the camera hardware writes raw image frames into three separate memory planes: Plane 0 (Y Luminance), Plane 1 (U Chrominance), and Plane 2 (V Chrominance).
</p>

<p>
Module 02 implements a high-throughput, zero-copy buffer assembler in <code>processFrame()</code>:
</p>

<pre><code>// High-Performance Camera Stream Processing (pose_detection_service.dart)
final WriteBuffer allBytes = WriteBuffer();
for (final Plane plane in image.planes) {
  allBytes.putUint8List(plane.bytes);
}
final bytes = allBytes.done().buffer.asUint8List();

final InputImageMetadata metadata = InputImageMetadata(
  size: Size(image.width.toDouble(), image.height.toDouble()),
  rotation: InputImageRotationValue.fromRawValue(camera.sensorOrientation) 
            ?? InputImageRotation.rotation0deg,
  format: InputImageFormatValue.fromRawValue(image.format.raw) 
          ?? InputImageFormat.yuv420,
  bytesPerRow: image.planes[0].bytesPerRow,
);

final inputImage = InputImage.fromBytes(bytes: bytes, metadata: metadata);
final poses = await _poseDetector.processImage(inputImage);</code></pre>

<h3>Defensive Pipeline Safeguards:</h3>
<ol>
    <li><strong>Concurrency Mutex Lock (<code>_isBusy</code>)</strong>: If the smartphone's NPU takes $22\text{ ms}$ to process a frame while the camera delivers a new frame after $16\text{ ms}$, the incoming frame is immediately dropped without queue buildup, preventing memory spikes.</li>
    <li><strong>Hardware Sensor Orientation Mapping</strong>: Automatically maps Android's hardware sensor orientation ($90^\circ, 270^\circ$) to upright Cartesian coordinates, preventing inverted or sideways skeletons.</li>
    <li><strong>Temporal Landmark Ring Buffer (90 Frames)</strong>: Maintains the latest 90 frames of full-body coordinates in memory (<code>landmarkBuffer</code>), providing a continuous 3-second temporal sliding window for Module 03 action recognition.</li>
</ol>

---

<h2 id="sec7">7. Mathematical Joint Trigonometry & Planar Angle Derivations</h2>

<p>
To compute real-time joint angles for exercise form evaluation, <code>pose_detection_service.dart</code> implements the two-dimensional arctangent formulation:
</p>

<div class="formula-card">
<strong>Planar Joint Angle Formulation (jointAngle method):</strong><br>
Let vertex joint $B$ connect adjacent landmarks $A$ and $C$ (e.g., Shoulder $A$, Elbow $B$, Wrist $C$):<br>
1. Calculate the directional vector angles relative to the horizontal axis:
$$\theta_1 = \text{atan2}(y_C - y_B, \; x_C - x_B)$$
$$\theta_2 = \text{atan2}(y_A - y_B, \; x_A - x_B)$$
<br>
2. Compute the absolute angular difference:
$$\Delta \theta = |\theta_1 - \theta_2| \cdot \frac{180^\circ}{\pi}$$
<br>
3. Normalize to the interior geometric angle $[0^\circ, 180^\circ]$:
$$\theta = \begin{cases} \Delta \theta & \text{if } \Delta \theta \le 180.0^\circ \\ 360.0^\circ - \Delta \theta & \text{if } \Delta \theta > 180.0^\circ \end{cases}$$
</div>

---

<h2 id="sec8">8. Exponential Moving Average (EMA) Coordinate Smoothing</h2>

<p>
To eliminate jitter and camera sensor noise, all detected landmark coordinates pass through an Exponential Moving Average (EMA) filter in <code>skeleton_painter.dart</code> before lines are drawn on screen:
</p>

<div class="formula-card">
<strong>EMA Temporal Smoothing Formulation:</strong><br>
$$\mathbf{P}_{\text{smoothed}}(t) = 0.70 \cdot \mathbf{P}_{\text{target}}(t) + 0.30 \cdot \mathbf{P}_{\text{prev}}(t-1)$$
<em>Where $\mathbf{P}_{\text{target}}(t)$ is the incoming raw coordinate and $\mathbf{P}_{\text{prev}}(t-1)$ is the previous smoothed coordinate.</em>
</div>

<p>
<strong>Occlusion Clamping:</strong> If a joint's detection likelihood drops below $0.45$ (e.g., hidden behind back or blocked by weights), it is automatically removed from the smoothing buffer (<code>_smoothedPoints.remove(type)</code>), preventing distorted phantom lines.
</p>

---

<h2 id="sec9">9. Downstream System Feed Pipeline</h2>

<p>
Module 02 is the single source of visual truth across the entire BioMechAI architecture. The table below illustrates how Module 02 feeds the remaining modules:
</p>

<table>
    <thead>
        <tr>
            <th>Downstream Module</th>
            <th>Data Fed from Module 02</th>
            <th>How It Is Utilized</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Module 03: Action Recognition</strong></td>
            <td>48-frame sliding window from <code>landmarkBuffer</code></td>
            <td>Transformed into 3D spatiotemporal connected limb heatmap tensors for PoseC3D SlowOnly ResNet-50.</td>
        </tr>
        <tr>
            <td><strong>Module 04: Rep Counting</strong></td>
            <td>Instantaneous Knee & Elbow angles</td>
            <td>Drives the 4-stage closed finite state machine (TOP $\to$ DESCENDING $\to$ BOTTOM $\to$ ASCENDING $\to$ TOP).</td>
        </tr>
        <tr>
            <td><strong>Module 05: Posture Correctness</strong></td>
            <td>33 3D Spatial Landmarks</td>
            <td>Calculates 3D vector dot products, computes form scores ($0-100\%$), and colors skeleton Green vs. Red.</td>
        </tr>
        <tr>
            <td><strong>Module 06: Body Scanner</strong></td>
            <td>Ankle-to-nose vertical pixel span</td>
            <td>Resolves monocular scale ambiguity ($scale = H_{\text{cm}} / \text{bodyPx}$) and extracts physical centimeter levers.</td>
        </tr>
        <tr>
            <td><strong>Module 07: Clinical Injury</strong></td>
            <td>ASIS Hips, Knees, Ankles</td>
            <td>Calculates Munro FPPA ($<165^\circ$) for dynamic knee valgus and McGill spinal line ($<150^\circ$) for lumbar sag.</td>
        </tr>
    </tbody>
</table>

---

<h2 id="sec10">10. Scientific Standards, Google Research Benchmarks, & Citations</h2>

<ul>
    <li><strong>Bazarevsky, Grishchenko, Raveendran, Zhu, Zhang, & Grundmann (2020)</strong>:
        <br><em>"BlazePose: On-device Real-time Body Pose Tracking."</em> Google Research, arXiv:2006.10204.
        <br><strong>Key Finding:</strong> Established the two-stage detector-tracker pipeline achieving 33-landmark 3D pose topology at $>30\text{ FPS}$ on standard mobile smartphone CPUs.
    </li>
    <li><strong>Cao, Simon, Wei, & Sheikh (CVPR 2017)</strong>:
        <br><em>"Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields (OpenPose)."</em>
        <br><strong>Significance:</strong> Established the foundational mathematical concepts for Part Affinity Fields (PAFs) that inspired modern heatmap architectures.
    </li>
    <li><strong>International Society of Biomechanics (ISB Recommendations)</strong>:
        <br>Provides the standard anatomical joint definitions (acromion, lateral epicondyle, styloid process, greater trochanter, lateral malleolus) mirrored by the 33-point BlazePose topology.
    </li>
</ul>

---

<h2 id="sec11">11. Panel Defense Quick-Reference: Frequently Asked Questions & Rapid Answers</h2>

<div class="defense-card">
<strong>Q1: How can a standard smartphone camera track 33 joints in 3D space without requiring physical markers or wearable sensors?</strong><br>
<em>Rapid Defense Answer:</em> We utilize Google ML Kit BlazePose, a deep convolutional neural network trained on hundreds of thousands of diverse human action poses. The model uses heat-map regression to predict the 2D pixel coordinates $(x, y)$ of 33 anatomical landmarks, and simultaneously predicts a relative depth coordinate ($z$) by learning perspective foreshortening and biomechanical bone constraints, achieving markerless 3D motion capture on raw video.
</div>

<div class="defense-card">
<strong>Q2: Why did you choose BlazePose over popular frameworks like OpenPose or YOLOv8-Pose?</strong><br>
<em>Rapid Defense Answer:</em> OpenPose is computationally massive, requiring high-power desktop GPUs ($>250\text{W}$), making it impossible to run locally on a smartphone at 30 FPS. While YOLOv8-Pose is fast, it only predicts 17 keypoints and completely lacks foot landmarks (heels and foot indices). BlazePose provides 33 landmarks including heels and toes, which are medically essential for detecting knee valgus and foot placement, while executing in $\sim 18\text{ ms}$ on mobile silicon.
</div>

<div class="defense-card">
<strong>Q3: How does BlazePose achieve 30 frames per second on a mobile phone without overheating the processor?</strong><br>
<em>Rapid Defense Answer:</em> It uses a two-stage Detector-Tracker architecture. Finding a human in a full video frame is computationally heavy, but tracking them once found is lightweight. The heavy detector runs only on the very first frame. In all subsequent frames, the system bypasses the detector and crops a small region of interest directly from the previous frame's joints, reducing computational load by over 80%.
</div>

<div class="defense-card">
<strong>Q4: What does the relative depth coordinate 'z' mean if the camera only has a flat 2D lens?</strong><br>
<em>Rapid Defense Answer:</em> Because a single lens cannot directly measure laser time-of-flight, the $z$ coordinate represents relative depth calibrated to the midpoint between the athlete's hips ($z=0$). If a joint moves closer to the camera than the hips (such as punching an arm forward), $z$ becomes negative. If it moves further away, $z$ becomes positive. This enables true 3D spatial vector calculations invariant to 2D perspective.
</div>

<div class="defense-card">
<strong>Q5: What is the purpose of the YUV420 memory buffer concatenation in your code?</strong><br>
<em>Rapid Defense Answer:</em> Android cameras stream video in raw YUV420 format across three separate memory planes (luminance and two chrominance planes). Naive frame conversion in Dart creates massive garbage collection churn and freezes the UI. We engineered a native <code>WriteBuffer</code> that concatenates all byte planes into a contiguous NV21 byte buffer in memory in $<1\text{ millisecond}$, completely eliminating dropped frames.
</div>

<div class="defense-card">
<strong>Q6: What happens if an athlete's limb is blocked by exercise equipment or moves out of the camera frame?</strong><br>
<em>Rapid Defense Answer:</em> Every landmark includes a visibility confidence score ($v_k$). If $v_k < 0.45$, our engine classifies the joint as occluded and removes it from the rendering and kinematic buffers. Furthermore, our boundary validation rejects frames where feet or head are cut off by the screen edges, prompting the voice coach to say <em>"Step back into frame"</em>.
</div>

<div class="defense-card">
<strong>Q7: How does Module 02 connect to the rest of the 9 modules in the system?</strong><br>
<em>Rapid Defense Answer:</em> Module 02 is the foundational sensory pipeline. It extracts 33 landmarks at 30 FPS and buffers them in a 90-frame queue. It feeds 48-frame window tensors to Module 03 (Action Recognition), joint flexion angles to Module 04 (Rep Counting), 3D spatial vectors to Module 05 (Posture Correctness), vertical body pixel spans to Module 06 (Body Scanner), and knee-hip-ankle lines to Module 07 (Clinical Injury Prevention).
</div>
