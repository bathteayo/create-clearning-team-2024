# Create Creaning-Team

This repository can create cleaning-team for azumi lab.

## 1. Install

### 1.1. Clone this repository

```bash
git clone https://github.com/yunicoder/create-clearning-team.git
```

### 1.2. Install python library

if you use pip:

```bash
pip install -r requirements.txt
```

if you use conda:

```bash
conda env create --file conda.yml
conda activate cct_env
```

## 2. Usage

Executing following command, then you can create **five** groups that meet the criteria (shown in [Sec. 3](#3-criteria)).

```bash
python main.py --group_num 5
```

Following results files will be generated!

```plaintext
results/created_team.yaml
results/output_team_for_slack
```

## 3. Criteria

### 3.1. English

- At least one person from each grade is included in a group.
- The person who has been in the same group is not in the same group.
  - If no solution can be found in 200,000 loops, the combination with the fewest number of same pair is chosen.

### 3.2. 日本語

- 各グループに各学年最低一人以上はいる
- これまで同じグループになった人とは同じグループにならない
  - もしも200,000ループ以内に条件を満たす解が見つからない場合、これまで同じグループになったことがあるペア数が最も少ない組み合わせが選ばれる
