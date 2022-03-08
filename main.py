import argparse
import yaml

from decide_team import DecideTeam

def output_team_yaml(team):
    team_dict = dict()
    for i, group in enumerate(team):
        team_dict[f"g{i+1}"] = group
    with open("results/created_team.yaml", "w", encoding="utf-8") as file:
        yaml.dump(team_dict, file, default_flow_style=False)
    

def main(args):
    decide_team = DecideTeam(args.group_num)

    team, not_first_cnt = decide_team.decide_team()

    print("------ decide team! ------")
    print(f"既に同じグループになったことのある組み合わせの数 : {not_first_cnt}")
    print(team)

    output_team_yaml(team)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group_num', type=int, default=4, help='グループの数')
    args = parser.parse_args()

    main(args)
