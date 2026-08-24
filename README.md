<div align="center">
<img src="./assets/banner.svg" width="100%" alt="Kaushal S — AI Systems × Security × Edge"/>
</div>

<div align="center">

<a href="https://kaushalrog.github.io/portfolio"><img src="https://img.shields.io/badge/PORTFOLIO-00E5FF?style=flat-square&logo=vercel&logoColor=0A0A18&labelColor=0A0A18"/></a>
<a href="https://linkedin.com/in/kaushal-s-19234b314"><img src="https://img.shields.io/badge/LINKEDIN-FF2E92?style=flat-square&logo=linkedin&logoColor=0A0A18&labelColor=0A0A18"/></a>
<a href="https://github.com/kaushalrog/kaushal-api"><img src="https://img.shields.io/badge/THIS_README_IS_A_SERVICE-8B5CF6?style=flat-square&logo=githubactions&logoColor=0A0A18&labelColor=0A0A18"/></a>
<a href="https://buymeacoffee.com/kaushalrog"><img src="https://img.shields.io/badge/FUEL_ME-FFD23F?style=flat-square&logo=buy-me-a-coffee&logoColor=0A0A18&labelColor=0A0A18"/></a>

<sub>
<a href="#status">status</a> ·
<a href="#whoami">whoami</a> ·
<a href="#builds">builds</a> ·
<a href="#feed">feed</a> ·
<a href="#ci">ci</a> ·
<a href="#evidence">evidence</a> ·
<a href="#skills">skills</a> ·
<a href="#telemetry">telemetry</a> ·
<a href="#offduty">off-duty</a>
</sub>

</div>

<img src="./assets/rule.svg" width="100%"/>

<a name="status"></a>
### `root@amrita:~$ systemctl status kaushal`

<!--START:SYSTEM_STATUS-->
```
┌─ SYSTEM STATUS ────────────────────────────┐
│ ● ONLINE                                   │
│                                            │
│ repositories    18                         │
│ stars           56                         │
│ followers       23                         │
│ active builds   2                          │
│ contributions   723 (12mo)                 │
│ streak          4 days                     │
│                                            │
│ last activity                              │
│ └── Smart-India-Hackathon-2026 · 10 hours  │
└────────────────────────────────────────────┘
```
<!--END:SYSTEM_STATUS-->

<img src="./assets/rule.svg" width="100%"/>

<a name="whoami"></a>
### `root@amrita:~$ whoami`

I build intelligent systems that have to survive real-world constraints — attackers, latency budgets, unreliable sensors, and their own uncertainty. Security-first AI, not AI with security bolted on.

IEEE-published on autonomous robotics. Building intrusion detection that scores behavioral drift in under 12ms on a Raspberry Pi 5, and RAG systems that abstain instead of hallucinating an answer.

<img src="./assets/rule.svg" width="100%"/>

<a name="builds"></a>
### `root@amrita:~$ top -p projects`

<!--START:PROJECT_TABLE-->
```
┌─ top -p projects ──────────────────────────────────────┐
│ PID   PROJECT       STATUS     SIGNAL                  │
│                                                        │
│ 001   WDS-IDS       RESEARCH   ░░░░░░░░░░              │
│ 002   SciRAG-UQ     BUILDING   ░░░░░░░░░░              │
│ 003   TrafficFlow   ACCEPTED   ░░░░░░░░░░              │
│ 004   AntBot        PUBLISHED  ░░░░░░░░░░              │
│                                                        │
│ signal = commits in the last 30 days (peak 0)          │
└────────────────────────────────────────────────────────┘
```
<!--END:PROJECT_TABLE-->

<table>
<tr><th align="left">module</th><th align="left">status</th><th align="left">detail</th></tr>
<tr valign="top">
<td>🛡️<br><b>WDS-IDS</b></td>
<td><code>RESEARCH</code></td>
<td>Behavioral intrusion detection with no payload inspection — telemetry collector, drift scorer, and alert layer as independent services on a Raspberry Pi 5.<br><i>Measured on SRBH-20 (web attacks) under five-fold cross-validation: perfect recall and AUC 1.00, end-to-end latency under 12ms. A saturated score on a single benchmark says as much about the dataset as the detector — cross-dataset evaluation is the current work.</i><br><code>[CODE]</code> github.com/kaushalrog/ids-System</td>
</tr>
<tr valign="top">
<td>🧠<br><b>SciRAG-UQ</b></td>
<td><code>RESEARCH — in progress</code></td>
<td>Uncertainty-aware RAG for scientific literature synthesis. Three-signal confidence — retrieval, NLI contradiction, self-consistency — Platt-scaled into a threshold that decides when to abstain.<br><code>[CODE]</code> github.com/kaushalrog/SciRAG-UQ</td>
</tr>
<tr valign="top">
<td>🕷️<br><b>AntBot</b></td>
<td><code>PUBLISHED</code></td>
<td>Low-cost 18-DOF hexapod surveillance platform with biologically inspired gait planning, built against cost and mobility constraints.<br><code>[PAPER]</code> ieeexplore.ieee.org/abstract/document/11426098</td>
</tr>
<tr valign="top">
<td>🚦<br><b>TrafficFlow AI</b></td>
<td><code>ACCEPTED</code></td>
<td>Adaptive traffic signal control — LSTM, Random Forest, LightGBM and fuzzy logic in a hybrid predictor, with a real-time congestion dashboard.<br><code>[VENUE]</code> ICPEEV 2026, Mahindra University · <code>[CODE]</code> github.com/kaushalrog/TrafficFlowAI</td>
</tr>
</table>

<img src="./assets/rule.svg" width="100%"/>

<a name="feed"></a>
### `root@amrita:~$ journalctl -u kaushal`

<!--START:BUILD_FEED-->
```
┌─ journalctl -u kaushal ────────────────────────────────┐
│ 10 hours ago  PUSH     Smart-India-Hackathon-2026      │
│               └── 0 commits                            │
│ 5 days ago    PUSH     AG-DATA                         │
│               └── 0 commits                            │
│ 6 days ago    PUSH     kaushalrog                      │
│               └── 0 commits                            │
│ 6 days ago    PUSH     AG-DATA                         │
│               └── 0 commits                            │
│ 7 days ago    STAR     deepseek-harness                │
│ 8 days ago    STAR     OmniRoute                       │
│ 9 days ago    PUSH     AG-DATA                         │
│               └── 0 commits                            │
│ 9 days ago    CREATE   AG-DATA                         │
│               └── branch main                          │
└────────────────────────────────────────────────────────┘
```
<!--END:BUILD_FEED-->

<img src="./assets/rule.svg" width="100%"/>

<a name="ci"></a>
### `root@amrita:~$ systemctl status --failed`

<!--START:CI_STATUS-->
```
┌─ CI STATUS ────────────────────────────────┐
│ · WDS-IDS       no CI                      │
│ · SciRAG-UQ     no CI                      │
│ ✓ TrafficFlow   passing                    │
│ · AntBot        no CI                      │
└────────────────────────────────────────────┘
```
<!--END:CI_STATUS-->

<img src="./assets/rule.svg" width="100%"/>

<a name="evidence"></a>
### `root@amrita:~$ cat evidence.log`

```
[PUBLICATION]   IEEE, Jan 2026 ............ AntBot hexapod surveillance
[ACCEPTED]      ICPEEV 2026 ............... TrafficFlow AI
[SUBMITTING]    BDA 2026 (target) ......... SciRAG-UQ
[OPEN SOURCE]   Vulkan-Loader ............. 5 verified fixes (C)
                Atomic Red Team ........... 12 fixes (Python/Ruby)
                MITRE CTI ................. validator + Actions CI
```

<img src="./assets/rule.svg" width="100%"/>

<a name="skills"></a>
### `root@amrita:~$ dpkg --list | grep skills`

<table>
<tr><td valign="top"><b>LANGUAGES</b></td><td>Python · C++ · Java · SQL · Bash</td></tr>
<tr><td valign="top"><b>AI / ML</b></td><td>PyTorch · TensorFlow · scikit-learn · LightGBM · LSTM</td></tr>
<tr><td valign="top"><b>LLM SYSTEMS</b></td><td>RAG · Agentic AI · Transformers · MCP · FAISS · ChromaDB · Uncertainty Quantification</td></tr>
<tr><td valign="top"><b>SECURITY</b></td><td>Intrusion Detection · Behavioral Analysis · Drift Detection · Kali Linux</td></tr>
<tr><td valign="top"><b>SYSTEMS</b></td><td>Linux · Docker · FastAPI · Microservices · REST APIs</td></tr>
<tr><td valign="top"><b>EDGE / ROBOTICS</b></td><td>Raspberry Pi · Arduino · Edge Computing · Gait Planning</td></tr>
</table>

<a name="telemetry"></a>
<!--START:STACK_TELEMETRY-->
```
┌─ LANGUAGE MIX ─────────────────────────────────────────┐
│ Jupyter Notebook 42.2%  ██████████████                 │
│ HTML           22.7%  ████████░░░░░░                   │
│ Python         19.9%  ███████░░░░░░░                   │
│ TypeScript      8.9%  ███░░░░░░░░░░░                   │
│ Scala           2.9%  █░░░░░░░░░░░░░                   │
│ TeX             1.6%  █░░░░░░░░░░░░░                   │
│                                                        │
│ share of bytes across own public repos                 │
└────────────────────────────────────────────────────────┘
```
<!--END:STACK_TELEMETRY-->

<img src="./assets/rule.svg" width="100%"/>

<a name="offduty"></a>
### `root@amrita:~$ man kaushal | grep -A2 "off duty"`

📸 Shooting campus events for Team Media, Amrita — full frame to full stack.
🏸 Badminton — the one arena where the loss function is honest.
📖 Reading papers I'll probably try to break in six months.

<img src="./assets/rule.svg" width="100%"/>

<sub>Panels above are generated from the GitHub API by <a href="https://github.com/kaushalrog/kaushal-api">kaushal-api</a> and committed by a scheduled workflow. Last run: 2026-08-24T18:23:19Z</sub>

```
root@amrita:~# exit
connection closed.
```
