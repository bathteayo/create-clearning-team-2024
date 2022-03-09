# Create Creaning-Team
This repository can create cleaning-team for azumi lab.

## 1. Install
1.1. Clone this repository
```
$ git clone https://github.com/yunicoder/create-clearning-team.git
```

1.2. Install python library
```
# if you use pip:
$ pip install -r requrements.txt

# if you use conda:
$ conda env create --file conda.yml
$ conda activate cct_env
```


## 2. Usage
You can create **five** group that meet the criteria (shown in 3. section).
```
$ python main.py --group_num 5
```

Following result files will be generated!
```
results/created_team.yaml
results/output_team_for_slack
```

## 3. Criteria 

### 3.1. English
- At least one person from each grade is included in a group.
- The person who has been in the same group is not in the same group.
    - If no solution can be found in 200000 loops, the combination with the fewest number of same pair is choiced.
### 3.2. Japanese
- 各グループに各学年最低一人以上はいる
- これまで同じグループになった人とは同じグループにならない
    - もしも20000ループ以内に条件を満たす解が見つからない場合、これまで同じグループになったことがあるペア数が最も少ない組み合わせが選ばれる

