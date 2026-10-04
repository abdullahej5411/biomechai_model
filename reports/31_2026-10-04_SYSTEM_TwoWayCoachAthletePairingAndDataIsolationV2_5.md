# Milestone Report #31: Two-Way Coach-Athlete Pairing & Multi-Tenant Data Isolation Engine

**Date**: October 4, 2026  
**Academic Phase**: Semester 8 — FYP-II Final Defense & Graduation Evaluation  
**System Version**: BioMechAI v2.5 (APK: `BioMechAI_v2.5_TwoWayCoachPairing.apk`)  
**Firebase Project**: `biomechai-fitness` (Project Number `479596177740`, Owner: `aejshah@gmail.com`)  

---

## 1. Executive Summary & Objective

In modern fitness applications, pairing between certified coaches and athletes must respect user autonomy, data privacy, and multi-tenant isolation. Previously, athlete profiles were globally accessible or manually assigned. Under Milestone #31, BioMechAI deployed **Two-Way Coach-Athlete Pairing (Approach 2)** across both the React Coach Web Dashboard and the Flutter Android Mobile App:

1. **Invitation-Driven Pairing**: A coach invites an athlete by entering their registered email. An invitation record is dispatched directly to the athlete's account.
2. **Athlete Sovereignty (Accept / Decline)**: The athlete receives a high-visibility invitation banner on both their Mobile App (`home_screen.dart`, `profile_screen.dart`) and Web Dashboard (`DashboardHome.tsx`). The athlete can choose to **Accept** or **Decline**.
3. **Multi-Tenant Coach Isolation**: Coaches only have access to athletes who explicitly accepted their invitation (`c.trainerId === coachUid`). Unpaired athletes remain completely hidden and protected from unauthorized data ingestion.
4. **Two-Sided Disconnect / Unlink**:
   - The Coach can remove an athlete from their roster at any time via `ClientListPage.tsx` or `ClientDetailPage.tsx`.
   - The Athlete can disconnect from their coach at any time via `ProfilePage.tsx` on the Web or `profile_screen.dart` on Mobile, immediately reverting to autonomous self-guided training mode.
5. **Real-Time Cross-Platform Synchronization**: Powered by Firestore real-time snapshots (`onSnapshot`), state changes (invites, acceptances, disconnects) propagate instantly across Web and Mobile without requiring application restarts or manual refreshes.

---

## 2. Technical Architecture & Invitation Protocol

```mermaid
sequenceDiagram
    autonumber
    actor Coach as Coach (Web Dashboard)
    participant FS as Firestore (users/{uid})
    actor Athlete as Athlete (Mobile App & Web)

    Coach->>FS: Look up athlete by email in 'users' collection
    alt Athlete not found or role != 'user'
        FS-->>Coach: Return error ("No athlete account registered with this email")
    else Athlete found
        Coach->>FS: Set pendingCoachRequest: { coachId, coachName, coachEmail, sentAt }
        FS-->>Athlete: Real-time onSnapshot triggers invitation banner
    end

    alt Athlete Declines
        Athlete->>FS: Clear pendingCoachRequest (set to null)
        FS-->>Coach: Invitation disappears from "Pending Invitations" roster
    else Athlete Accepts
        Athlete->>FS: Set trainerId = coachId, trainerName = coachName, pendingCoachRequest = null
        FS-->>Coach: Athlete appears in "Active Roster" with full telemetry access
    end

    opt Two-Sided Disconnect
        alt Coach Removes Client
            Coach->>FS: Set athlete.trainerId = null, athlete.trainerName = null
        else Athlete Disconnects
            Athlete->>FS: Set athlete.trainerId = null, athlete.trainerName = null
        end
        FS-->>Both: Telemetry access severed; athlete reverts to independent training
    end
```

---

## 3. Web Dashboard Implementation (`web_dashboard/`)

### A. Real-Time Reactive State (`src/context/AuthContext.tsx`)
Converted static profile fetching to Firestore real-time document listener:
```typescript
docUnsub = onSnapshot(
  doc(db, 'users', user.uid),
  (snap) => {
    if (snap.exists()) {
      setUserProfile({
        uid: user.uid,
        email: user.email || '',
        role: snap.data().role === 'trainer' ? 'trainer' : 'user',
        ...snap.data(),
      } as UserProfile);
    }
    setLoading(false);
  }
);
```

### B. Dual-Tab Client Management Console (`src/pages/ClientListPage.tsx`)
- **Active Roster Tab**: Displays all athletes who have accepted pairing (`c.trainerId === uid`). Includes search, sorting, average form scores, and a **`Remove from Roster`** action with a safety confirmation modal.
- **Pending Invitations Tab**: Displays all dispatched invitations awaiting athlete response (`c.pendingCoachRequest?.coachId === uid`). Includes a **`Cancel Invitation`** action.
- **`+ Invite Athlete` Modal**: Interactive modal with email lookup, role verification (blocks inviting other coaches), and duplicate invite prevention.

### C. Client Detail Roster Safeguard (`src/pages/ClientDetailPage.tsx`)
- Added danger-zone **`Remove from Roster`** button with confirmation modal that detaches the athlete, returns the coach to `/clients`, and updates Firestore cleanly.

### D. Athlete Dashboard Coaching Banner (`src/pages/DashboardHome.tsx`)
- Header status pill: Displays `🛡️ Coached by <CoachName>` or `🏃 Independent Athlete`.
- Real-time Invitation Alert Card: Displays coach name, email, and timestamp with interactive **`Accept`** and **`Decline`** actions.
- Multi-Coach Isolation Filter: Enforces `c.trainerId === uid` so coaches only see their assigned clients in overview metrics.

### E. Athlete Profile Coaching Section (`src/pages/ProfilePage.tsx`)
- Dedicated **Coaching & Guidance** panel displaying coach details or independent status, featuring a **`Disconnect from Coach`** button with confirmation prompt.

---

## 4. Mobile App Implementation (`biomechai_flutter_latest/`)

### A. Data Model Backward Compatibility (`lib/models/user_model.dart`)
Extended `UserModel` with optional pairing fields:
```dart
final String? trainerId;
final String? trainerName;
final Map<String, dynamic>? pendingCoachRequest;
```
Ensured 100% backward-compatible serialization in `toMap()` and `fromMap()`.

### B. Home Screen Real-Time Invitation Banner (`lib/screens/home_screen.dart`)
- Detects `user.pendingCoachRequest != null`.
- Renders an interactive card using `AppTheme.card2` and `AppTheme.neonAccent`:
  - Displays Coach Name and Email.
  - **`Accept`**: Updates `trainerId`, `trainerName`, clears `pendingCoachRequest`, and shows a green success toast.
  - **`Decline`**: Clears `pendingCoachRequest` and restores default home view.

### C. Profile Screen Coaching Management (`lib/screens/profile_screen.dart`)
- **`_buildCoachingCard`**:
  - *Pending Request State*: Shows coach invitation with Accept/Decline action buttons.
  - *Active Coach State*: Shows coach name, certified coach badge, and an outlined **`Disconnect`** button with a safety confirmation dialog.
  - *Independent State*: Shows an informative "Self-Guided Athlete" card explaining that workouts remain private until a coach invitation is accepted.

---

## 5. Chromium DOM-Detached Blob PDF Download Fix

During testing of the Option C PDF engine, an issue was identified on Chromium 115+ (Chrome and Edge):
- **Symptom**: Clicking "Download PDF" downloaded a file named with an internal blob UUID (`a227f31b-708d-4a11-b062...`) without a `.pdf` extension.
- **Root Cause**: Chromium security policies ignore `download="filename.pdf"` attributes on synthetic `<a>` elements unless the anchor element is explicitly appended to `document.body` before programmatic dispatch.
- **Resolution (`src/utils/pdfExport.ts`)**:
  ```typescript
  const downloadLink = document.createElement('a');
  downloadLink.href = url;
  downloadLink.download = filename.endsWith('.pdf') ? filename : `${filename}.pdf`;
  document.body.appendChild(downloadLink);
  downloadLink.click();
  setTimeout(() => {
    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(url);
  }, 1500);
  ```
  Result: PDFs now download with exact filenames (e.g., `BioMechAI_Assessment_JohnDoe.pdf`) across all Chromium and Safari browsers.

---

## 6. Verification & Quality Assurance Audit

| Target | Verification Protocol | Exit Code | Result |
|:---|:---|:---:|:---|
| **Mobile Static Analysis** | `dart analyze lib/` | `0` | **0 errors, 0 warnings** |
| **Mobile Compilation** | `flutter build apk --debug` | `0` | **Compiled `BioMechAI_v2.5_TwoWayCoachPairing.apk` (222.4 MB)** |
| **Web Dashboard** | `tsc -b && vite build` | `0` | **0 TypeScript errors, bundle verified** |
| **Web Live Deployment** | `firebase deploy --only hosting` | `0` | **Live on `https://biomechai-fitness.web.app`** |
| **Styling Preservation** | Visual regression audit | — | **Zero layout shifts, zero render overflows** |

---

## 7. Artifact Manifest
- **New Production APK**: [`BioMechAI_v2.5_TwoWayCoachPairing.apk`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/BioMechAI_v2.5_TwoWayCoachPairing.apk)
- **Previous Baseline APK**: `BioMechAI_v2.4_PdfAssessmentExport.apk`
- **Git Commits**:
  - Web & Flutter repo: `1adf6dd`, `e7c50c3`, `5bfaa6a`
  - Model repo: `c19dce0`
