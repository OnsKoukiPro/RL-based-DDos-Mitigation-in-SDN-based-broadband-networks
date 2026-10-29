<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/banner-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/banner-light.svg?v=r1" alt="RL × SDN: a software-defined network that watches its own flow tables and learns when to drop a flood" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/stats-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/stats-light.svg?v=r1" alt="94.6% accuracy with a decision tree, 0.997 precision, 3 flow features, 3 second polling loop" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/s1-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/s1-light.svg?v=r1" alt="01 / Control loop: watch, decide, drop" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/loop-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/loop-light.svg?v=r1" alt="Control loop: Mininet switches report flow stats to the Ryu controller every 3 s; features feed a detector whose decision installs a drop rule" width="100%"></picture>

A Ryu OpenFlow 1.3 controller polls flow statistics every 3 s and turns them into three cheap features: **SFE** (speed of flow entries), **SSIP** (speed of source IPs) and **RFIP** (ratio of pair flows). A supervised classifier or an RL agent (tabular Q-learning, DDPG) decides, and the controller installs a drop rule on the ingress port.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/s2-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/s2-light.svg?v=r1" alt="02 / Data: floods stand out" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/scatter-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/scatter-light.svg?v=r1" alt="Scatter of 3,580 polling windows: normal traffic stays small, ICMP floods spread over four orders of magnitude" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/s3-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/s3-light.svg?v=r1" alt="03 / Results: how well it blocks" width="100%"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/bars-dark.svg?v=r1"><img src="https://raw.githubusercontent.com/OnsKoukiPro/RL-based-DDos-Mitigation-in-SDN-based-broadband-networks/master/.github/assets/bars-light.svg?v=r1" alt="Decision tree vs SVM: accuracy 0.946 vs 0.844, precision 0.997 vs 1.000, recall 0.875 vs 0.630, F1 0.932 vs 0.773" width="100%"></picture>

Supervised baseline, 5-fold stratified CV on 3,580 samples (1,515 attack, 2,065 normal): `python evaluate_baseline.py`. Very few false positives; recall is the weak point.

<details>
<summary><b>Files</b></summary>

| What | Files |
|---|---|
| Traffic | `normal-traffic.sh` (benign pings), `attack-traffic.sh` (`hping3 --rand-source` ICMP floods) |
| Data collection | controller with `APP_TYPE = 0` logs `sfe, ssip, rfip, label` to `result.csv` |
| Supervised | `normal-traffic-detection.py`, `attack-traffic-detection.py`, `svm_model.py` |
| Q-learning | `m_attack_rl.py` + `rl_model2.py` (ε-greedy, allow/block) |
| DDPG | `m_attack_rl2.py` + `rl_model3.py` (actor-critic, Ornstein-Uhlenbeck exploration) |
| Analysis | `perf_analysis.py` (TP/FP/TN/FN, flow count vs detections) |

</details>

<details>
<summary><b>Run it</b></summary>

Linux with Mininet, Open vSwitch, Ryu and hping3.

```bash
ryu-manager attack-traffic-detection.py      # terminal 1, or m_attack_rl.py for the RL agent
sudo python2 attack-traffic-topo.py && sudo mn -c    # terminal 2

pip install -r requirements.txt && python evaluate_baseline.py   # offline evaluation
```

</details>

**Next:** compute the RL reward from the generator's ground-truth labels instead of the agent's own mitigation flag, then benchmark it against the baseline; turn on port blocking in the RL controller; larger topology and SYN/UDP floods.
