import argparse

from decide_team import DecideTeam

def main(args):
    decide_team = DecideTeam(args.group_num)

    team, not_first_cnt = decide_team.decide_team()

    print("------ decide team! ------")
    print(f"既に同じグループになったことのある組み合わせの数 : {not_first_cnt}")
    print(team)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group_num', type=int, default=5, help='グループの数')
    args = parser.parse_args()

    main(args)
