import argparse
import tomlkit as toml

from decide_team import DecideTeam

def output_team_toml(team):
    team_dict = dict()
    for i, group in enumerate(team):
        team_dict[f"g{i+1}"] = group
    with open("results/created_team.toml", "w", encoding="utf-8") as f:
        toml.dump(team_dict, f)

def output_slack(team):
    output_str = ""
    for i, group in enumerate(team):
        output_str += f"{i+1}. "
        for member in group:
            output_str += f"@{member} "
        output_str += "\n"
    with open("results/output_team_for_slack.txt", "w", encoding="utf-8") as f:
        print(output_str, file=f)

def main(args):
    decide_team = DecideTeam(args.group_num)
    team, not_first_cnt = decide_team.decide_team()

    print("------ decide team! ------")
    print(f"既に同じグループになったことのある組み合わせの数 : {not_first_cnt}")
    print(team)

    output_team_toml(team)
    output_slack(team)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group_num', type=int, default=4, help='グループの数')
    args = parser.parse_args()

    main(args)
