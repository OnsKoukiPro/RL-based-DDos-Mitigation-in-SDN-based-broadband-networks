# RL-based DDoS Detection & Mitigation in SDN

Research prototype: detect and mitigate ICMP-flood DDoS attacks in a software-defined network. A Ryu OpenFlow 1.3 controller polls flow statistics from the switches, extracts traffic features, and decides whether to block. The decision comes from either a supervised classifier or a reinforcement-learning agent.

## How it works

```
 Mininet topology (2 OVS switches, hosts h1..hN)
        │  OpenFlow 1.3 flow-stats every 3 s
        ▼
 Ryu controller ──► feature extraction ──► detector ──► mitigation
                    SFE  speed of flow entries      DecisionTree / SVM   drop rule on
                    SSIP speed of source IPs        Q-learning agent     ingress port
                    RFIP ratio of pair-flows        DDPG agent (exp.)    (120 s hard timeout)
```

- **Traffic generation**: `normal-traffic.sh` (benign pings between hosts), `attack-traffic.sh` (`hping3 --rand-source` ICMP floods at varying rates).
- **Data collection**: run the controller with `APP_TYPE = 0` to log `sfe, ssip, rfip, label` rows into `result.csv`.
- **Detection**:
  - `normal-traffic-detection.py`, `attack-traffic-detection.py`: supervised baseline (`svm_model.py`, Decision Tree / SVM)
  - `m_attack_rl.py` + `rl_model2.py`: tabular Q-learning agent (ε-greedy, actions allow/block)
  - `m_attack_rl2.py` + `rl_model3.py`: DDPG actor-critic agent (continuous action, Ornstein-Uhlenbeck exploration)
- **Analysis**: `perf_analysis.py` computes TP/FP/TN/FN and plots flow count against detections.

## Results: supervised baseline

Run `python evaluate_baseline.py` for 5-fold stratified CV on the 3,580 collected samples (1,515 attack / 2,065 normal):

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Decision Tree | 0.946 | 0.997 | 0.875 | 0.932 |
| SVM (RBF) | 0.844 | 1.000 | 0.630 | 0.773 |

Three cheap flow-table features are enough to separate the attack traffic with very few false positives. Recall is the weak point.

## Run

Requires Linux with Mininet, Open vSwitch, Ryu and hping3.

```bash
# terminal 1: controller
ryu-manager attack-traffic-detection.py      # or m_attack_rl.py for the RL agent

# terminal 2: topology + traffic
sudo python2 attack-traffic-topo.py && sudo mn -c

# offline evaluation
pip install -r requirements.txt
python evaluate_baseline.py
```

## Status & next steps

- The RL agents run online in the controller, but the reward still uses the agent's own mitigation flag. The next step is to compute it from the generator's ground-truth labels, then benchmark against the supervised baseline.
- Enable the port-blocking call in the RL controller once the reward is fixed.
- Larger topology and mixed attack types (SYN, UDP floods).

## Stack

Python, Ryu (OpenFlow 1.3), Mininet, Open vSwitch, scikit-learn, TensorFlow/Keras, hping3.
