
import numpy as np
import tomlkit as toml
import itertools
import random

class DecideTeam:

    def __init__(self, GROUP_NUM):
        self.GROUP_NUM = GROUP_NUM
        self.MAX_LOOP_CNT = 200000


    def load_config(self, path):
        with open(path, encoding="utf-8") as file:
            variables = toml.load(file).unwrap()
        return variables


    def create_team(self, members):
        cur_team = [[] for _ in range(self.GROUP_NUM)]

        member_list = list(itertools.chain.from_iterable(members.values()))  # 平滑化
        mem_num = len(member_list)

        ave_mem_num_per_group = mem_num / self.GROUP_NUM  # 1グループの平均メンバー数
        plus_one_group_num = mem_num % self.GROUP_NUM  # 平均より多く配置させないといけないグループ数
        plus_one_group_list = random.sample(range(self.GROUP_NUM), plus_one_group_num)  # 平均より多く配置させないといけないグループ
        
        # 学年ごとにグループを決定する
        for grade_mem in members.values():
            grade_mem_num = len(grade_mem)
            random.shuffle(grade_mem)

            ave_grade_mem_num_per_group = int(len(grade_mem) / self.GROUP_NUM)  # 今回の学年における一グループあたりの平均メンバー数 
            grade_plus_one_group_num = int(grade_mem_num % self.GROUP_NUM)  # 今回の学年における平均より多く配置させないといけないグループ数

            if grade_plus_one_group_num == 0:  # 全てのグループに平均数のメンバーを配置する場合
                # 順番にグループに追加
                cur_start_ind = 0
                for i in range(self.GROUP_NUM):
                    cur_end_ind = cur_start_ind + ave_grade_mem_num_per_group
                    cur_team_members = grade_mem[cur_start_ind:cur_end_ind]
                    cur_team[i].extend(cur_team_members)
                    cur_start_ind = cur_end_ind
            else:
                # 多く配置グループを決定
                cur_plus_one_groups = []  # 多く配置するグループ

                # (平均より多く配置するべき数)より(この学年で平均より多く配置するべき数)が上回ってしまっている時
                if len(plus_one_group_list) < grade_plus_one_group_num:
                    cur_plus_one_groups = plus_one_group_list
                    plus_one_group_list.clear()

                    # 配置しない場所は次以降で多く配置しないといけない
                    _cur_plus_one_groups = random.sample(range(self.GROUP_NUM), grade_plus_one_group_num-len(plus_one_group_list))
                    plus_one_group_list.extend(_cur_plus_one_groups)
                else:
                    cur_plus_one_groups = random.sample(plus_one_group_list, grade_plus_one_group_num)
                    for cur_plus_one_group in cur_plus_one_groups:
                        plus_one_group_list.remove(cur_plus_one_group)  # これから多く配置するのでリストから消去


                cur_start_ind = 0
                for i in range(self.GROUP_NUM):
                    if i in cur_plus_one_groups:  # 多く配置するべきグループ
                        cur_end_ind = cur_start_ind + ave_grade_mem_num_per_group + 1
                    else:
                        if ave_grade_mem_num_per_group == 0:
                            continue  # 一人も配置されない場合
                        cur_end_ind = cur_start_ind + ave_grade_mem_num_per_group
                    cur_team_members = grade_mem[cur_start_ind:cur_end_ind]
                    cur_team[i].extend(cur_team_members)
                    cur_start_ind = cur_end_ind
        return cur_team


    def extract_same_group_member(self, member, past_teams):
        same_group_member_list = []
        for past_team in past_teams.values():
            for group_member in past_team.values():
                if member in group_member:
                    same_group_member_list.extend(
                        [m for m in group_member if m!=member and m not in same_group_member_list]
                    )
        return same_group_member_list


    def check_each_member_meet_first(self, cur_team, past_teams):
        not_first_cnt = 0  # 初めてましてじゃない人の数
        for cur_group in cur_team:
            for mem in cur_group:
                same_group_member_list = self.extract_same_group_member(mem, past_teams)
                for cur_same_mem in cur_group:
                    if cur_same_mem in same_group_member_list:
                        not_first_cnt += 1
        if not_first_cnt == 0:
            return True, not_first_cnt
        else:
            return False, not_first_cnt


    def check_all_member_include_team(self, members, team):
        is_all_mem_include = True
        member_list = list(itertools.chain.from_iterable(members.values()))  # 平滑化

        for m in member_list:
            is_include = False
            for group in team:
                if m in group:
                    is_include = True
            if not is_include:
                print(f"{m}がチームにいません")
                is_all_mem_include = False
        
        return is_all_mem_include


    def decide_team(self):
        members = self.load_config("data/members.toml")
        past_teams = self.load_config("data/past-teams.toml")

        min_not_first_cnt_team = [] # 初めましてが最も少ないチーム
        min_not_first_cnt = np.inf

        loop_cnt = 0
        is_satisfy = False
        while not is_satisfy:
            cur_team = self.create_team(members)
            is_satisfy, not_first_cnt = self.check_each_member_meet_first(cur_team, past_teams)

            # 初めましてが最も少ないチームを更新
            if not_first_cnt < min_not_first_cnt:
                min_not_first_cnt = not_first_cnt
                min_not_first_cnt_team = cur_team

            loop_cnt += 1
            if loop_cnt >= self.MAX_LOOP_CNT:
                break

        # for debag
        self.check_all_member_include_team(members, min_not_first_cnt_team)

        return min_not_first_cnt_team, min_not_first_cnt
