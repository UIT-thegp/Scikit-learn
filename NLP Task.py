! wget https://dl.challenge.zalo.ai/news-summarization/data/public_test.zip
! unzip public_test.zip
!pip install vncorenlp
! wget https://github.com/vncorenlp/VnCoreNLP/archive/master.zip
! unzip master.zip
import pandas as pd
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', 1000)
test  = pd.read_json("/content/public_test/public_test/public_test.jsonl", lines = True)
from vncorenlp import VnCoreNLP
from collections import Counter
import pprint as pp
import json
vncorenlp_file = '/content/VnCoreNLP-master/VnCoreNLP-1.1.1.jar'
list_dict = []
for p in range(len(test)): #len(test)
  text = test['original_doc'][p]
  test_id = test['test_id'][p]
  size_temp = len(text["_source"]["body"])
  sentences = []
  for p in range(size_temp):
    temp = (text["_source"]["body"][p]["text"])
    if temp[len(temp)-1] != '.':
      temp += '.'
    sentences.append(temp)
    #pp.pprint(sentences)

  s = str()
  s = s + ' ' + ' '.join(sentences)
  s = s + '. ' + str(text["_source"]["description"])
  clean_text = s
  #pp.pprint(clean_text)
  #s = str(text["_source"]["description"])
  #sentences.clear()
  #sentences.append(s)
  #sentences.append(str(corpus["_source"]["description"]))"""
  #Scores
  scores =  []
  for j in range(len(clean_text)):
    if clean_text[j] == '-' and clean_text[j+2]!='-' and clean_text[j-2]!='-':
      if clean_text[j-1].isnumeric() and clean_text[j+1].isnumeric():
        scores.append(clean_text[j-1]+clean_text[j]+clean_text[j+1])
    if clean_text[j] == '-' and clean_text[j-2].isnumeric() and clean_text[j+2].isnumeric():
      scores.append(clean_text[j-2]+clean_text[j]+clean_text[j+2])
  #for j in range(len(clean_text)):
  #  if clean_text[j] == '-' and clean_text[j+2]!='-' and clean_text[j-2]!='-':
  #    if clean_text[j-1].isnumeric() and clean_text[j+1].isnumeric():
  #      scores.append(clean_text[j-1]+clean_text[j]+clean_text[j+1])
  #  if clean_text[j] == '-' or clean_text[j] == '–':
  #    if clean_text[j-2].isnumeric() and clean_text[j+2].isnumeric():
  #      scores.append(clean_text[j-2]+clean_text[j]+clean_text[j+2])
  listA = scores
  #print("Given List:\n",listA)
  if (len(listA) == 0):
    final_score_1 = 0
    final_score_2 = 0
  else :
    scores_occurence_count = Counter(listA)
    #print(list(scores_occurence_count))
    most_common_scores = list(scores_occurence_count.most_common())
    most_common_scores = [list(x) for x in most_common_scores]
    #print(most_common_scores)
    #Reverse
    i = 0
    while i < len(most_common_scores)-1:
      j = i+1
      while j < len(most_common_scores):
        if most_common_scores[j][0][0] in most_common_scores[i][0] and most_common_scores[j][0][2] in most_common_scores[i][0] and (int(most_common_scores[j][0][0]) + int(most_common_scores[j][0][2]) == int(most_common_scores[i][0][0])+int(most_common_scores[i][0][2])):
          #print(i,j)
          if most_common_scores[i][1] > most_common_scores[j][1]:
            #print(i,j)
            z = most_common_scores[j]
            cnt = most_common_scores[j][1]
            most_common_scores[i][1]+=cnt
            most_common_scores = [x for x in most_common_scores if x != z]
            i = 0
            break
          elif most_common_scores[i][1] < most_common_scores[j][1]:
            #print(i,j)
            z = most_common_scores[i]
            cnt = most_common_scores[i][1]
            most_common_scores[j][1]+=cnt
            most_common_scores = [x for x in most_common_scores if x != z]
            i = 0
            break
          else:
            #Pick Max
            #1st score:
            #if most_common_scores[i][0][0] > most_common_scores[j][0][0]:
            #  z = most_common_scores[j]
            #  cnt = most_common_scores[j][1]
            #  most_common_scores[i][1]+=cnt
            #  most_common_scores = [x for x in most_common_scores if x != z]
            #  i = 0
            #  break
            ##1st score:
            #else:
            #  z = most_common_scores[i]
            #  cnt = most_common_scores[i][1]
            #  most_common_scores[j][1]+=cnt
            #  most_common_scores = [x for x in most_common_scores if x != z]
            #  #print(most_common_scores)
            #  i = 0
            #  break
            #2nd score
            if most_common_scores[i][0][0] > most_common_scores[j][0][0]:
              z = most_common_scores[i]
              cnt = most_common_scores[i][1]
              most_common_scores[j][1]+=cnt
              most_common_scores = [x for x in most_common_scores if x != z]
              i = 0
              break
            else:
              z = most_common_scores[j]
              cnt = most_common_scores[j][1]
              most_common_scores[i][1]+=cnt
              most_common_scores = [x for x in most_common_scores if x != z]
              #print(most_common_scores)
              i = 0
              break
        j+=1
      i+=1
    most_common_scores.sort(key = lambda x : x[1],reverse= True)
    #print(most_common_scores)
    max_count = most_common_scores[0][1]
    #Pick Max (Value)
    most_common_scores = [x for x in most_common_scores if x[1] == max_count]
    if len(most_common_scores) == 1:
      final_score_1=most_common_scores[0][0][0]
      final_score_2=most_common_scores[0][0][2]
    if len(most_common_scores) == 0:
      final_score_1 = 0
      final_score_2 = 0
    else:
      for x in most_common_scores:
        x.append(max(int(x[0][0]),int(x[0][2])))
      #print(most_common_scores)
      most_common_scores.sort(key = lambda x : x[2],reverse = True)
      max_value = most_common_scores[0][2]
      most_common_scores = [x for x in most_common_scores if x[2] == max_value]
      final_score_1=most_common_scores[0][0][0]
      final_score_2=most_common_scores[0][0][2]
  with VnCoreNLP(vncorenlp_file) as vncorenlp:
    #print('Tokenizing:', vncorenlp.tokenize(sentences))
    #pos_tag = list(vncorenlp.pos_tag(s))
    ner = list(vncorenlp.ner(clean_text))
    #print('Dependency Parsing:', vncorenlp.dep_parse(sentences))
    #print('Annotating:', vncorenlp.annotate(sentences))
    #print('Language:', vncorenlp.detect_language(sentences))
  ner_merge = sum(ner,[])
  ner_merge = [list(x) for x in ner_merge]
  #ner_merge = [x for x in ]
  prefixes = [ 'các_cầu_thủ' ,'đt','đối_thủ', 'Đối_thủ', 'CLB', 'clb', 'Câu_lạc_bộ', 'câu_lạc_bộ'
             'lưới', 'đội_bóng', 'đội_bóng_chủ_nhà', 'các_cầu_thủ','cầu_thủ', 'tung_lưới', 'lưới', 'Lưới','đội_khách','tiếp_đón','đón']
  nations_prefixes = ['ĐT', 'Đội_tuyển','đội_tuyển','tuyển', 'Tuyển','đt']
  suffixes = ['United','united', 'Utd', 'utd', 'fc', 'FC', 'Fc']
  special_teams_prefixes = ['AC', 'AS']
  for i in range(len(ner_merge)):
    if (ner_merge[i][0] in prefixes or (ner_merge[i][0][0] == 'U' and len(ner_merge[i][0]) > 1 and ner_merge[i][0][1].isnumeric())) and ner and i!= len(ner_merge) - 1:
      if ner_merge[i][0][0].islower():
        if ner_merge[i+1][0][0].isupper():
          ner_merge[i+1][1] = 'B-ORG'
          if i+2 < len(ner_merge) -1 and ner_merge[i+2][0][0].isupper():
            ner_merge[i+2][1] = 'I-ORG'
            continue
      elif ner_merge[i+1][1] == 'I-ORG':
        continue
      elif ner_merge[i+1][1] != 'I-ORG' and ner_merge[i+1][0][0].isupper():
        ner_merge[i][1] = 'B-ORG'
        ner_merge[i+1][1] = 'I-ORG'
  for i in range(len(ner_merge)):
    if (ner_merge[i][0] in nations_prefixes) and i!= len(ner_merge) -1 and ner_merge[i][0][0].isupper():
      if ner_merge[i][0][0].isupper():
        ner_merge[i][1] = 'B-LOC'
        ner_merge[i+1][1] = 'I-LOC'
      else:
        ner_merge[i+1][1] = 'B-LOC'
  for i in range(len(ner_merge)-1):
    if ner_merge[i][0] in special_teams_prefixes:
      if ner_merge[i][1] != 'B-ORG':
        ner_merge[i][1] = 'B-ORG'
        ner_merge[i+1][1] = 'I-ORG'
  for i in range(len(ner_merge)):
    for s in suffixes:
      if s in ner_merge[i][0] and ner_merge[i][1] != 'I-ORG' and i != 0:
        if ner_merge[i-1][0][0].isupper() and ner_merge[i-1][0][0].isalpha():
          ner_merge[i][1] = 'I-ORG'
          ner_merge[i-1][1] = 'B-ORG'
        else :
          ner_merge[i][1] = 'B-ORG'
  i = 0
  while i<len(ner_merge)-1:
    if ner_merge[i][0] == 'khán_đài' and ner_merge[i+1][0][0].isupper():
      ner_merge[i][0] += '_'+ ner_merge[i+1][0]
      ner_merge.pop(i+1)
      i = 0
      continue
    i+=1
  i = 0
  while i<len(ner_merge)-1:
    if ner_merge[i][0] == 'vòng' and ner_merge[i+1][0] == 'bảng' and ner_merge[i+2][0][0].isupper():
      ner_merge[i][0] += '_'+ ner_merge[i+1][0] + '_'+ ner_merge[i+2][0]
      ner_merge.pop(i+1)
      ner_merge.pop(i+1)
      i = 0
      continue
    i+=1
  i = 0
  while i in range(len(ner_merge)-1):
    if (ner_merge[i][1] == 'B-ORG' or ner_merge[i][1] == 'B-LOC') and ner_merge[i+1][1] == 'B-PER':
      ner_merge[i][0] += ' '+ ner_merge[i+1][0]
      ner_merge.pop(i+1)
      i = 0
      continue
    i+=1
  soccer_team = [list(x) for x in ner_merge if (x[1] == 'B-ORG' or x[1] =='I-ORG' or x[1] =='B-LOC'or x[1] =='I-LOC')
  and x[0][0].isupper()]
  projected_soccer_team = [list(x) for x in ner_merge if x[1] == 'B-PER' or x[1] == 'I-PER' or
                         (x[1] == 'O' and x[0].isalnum() and x[0][0].isupper())]
  i = 0
  while i < len(projected_soccer_team)  :
    if i == len(projected_soccer_team) - 1 and projected_soccer_team[i][1] != 'I-LOC' and projected_soccer_team[i][1] != 'I-ORG' and projected_soccer_team[i][1] != 'I-PER' and projected_soccer_team[i][1] != 'O':
      break
    if projected_soccer_team[i][1] == 'B-PER' and projected_soccer_team[i+1][1] == 'I-PER':
      #print(i)
      projected_soccer_team[i][0] = projected_soccer_team[i][0] + ' '+ projected_soccer_team[i+1][0]
      projected_soccer_team.pop(i+1)
    i+=1
  #pp.pprint(projected_soccer_team )
  projected_soccer_team_candidates = []
  for i in range(len(projected_soccer_team)):
    temp_list = []
    temp_str = str()
    for j in range(len(projected_soccer_team[i][0])):
      if projected_soccer_team[i][0][j] != ' ' and projected_soccer_team[i][0][j] != '.' and projected_soccer_team[i][0][j] != '-' and projected_soccer_team[i][0][j] != '_':
        temp_str+=projected_soccer_team[i][0][j]
      else:
        if len(temp_str) != 0:
          temp_list.append(temp_str)
          temp_str = str()
          continue
      if j == len(projected_soccer_team[i][0]) -1:
        temp_list.append(temp_str)
        temp_str = str()
        projected_soccer_team_candidates.append(temp_list)
  #pp.pprint(soccer_team)
  candidates_trash_can = ['Diego','Lopez','HLV']
  targets = []
  for x in projected_soccer_team_candidates:
    for y in x:
      if y in candidates_trash_can:
        targets.append(x)
        #x = projected_soccer_team_candidates[0]
        break
  projected_soccer_team_candidates = [x for x in projected_soccer_team_candidates if x not in targets]
  #pp.pprint(projected_soccer_team_candidates)
  i = 0
  while i< (len(soccer_team)):
    if i == len(soccer_team) - 1 and soccer_team[i][1] != 'I-LOC' and soccer_team[i][1] != 'I-ORG' and soccer_team[i][1] != 'I-PER' and soccer_team[i][1] != 'O':
      break
    if soccer_team[i][1] == 'B-ORG' and soccer_team[i+1][1] == 'I-ORG':
      soccer_team[i][0] = soccer_team[i][0] + ' '+ soccer_team[i+1][0]
      soccer_team.pop(i+1)
    if soccer_team[i][1] == 'B-PER' and soccer_team[i+1][1] == 'I-PER':
      soccer_team[i][0] = soccer_team[i][0] + ' '+ soccer_team[i+1][0]
      soccer_team.pop(i+1)
      #continue
    if soccer_team[i][1] == 'B-LOC' and soccer_team[i+1][1] == 'I-LOC':
      if soccer_team[i][0][len(soccer_team[i][0])-1] == '.':
        soccer_team[i][0] = soccer_team[i][0] +soccer_team[i+1][0]
      else:
        soccer_team[i][0] = soccer_team[i][0] + ' ' +soccer_team[i+1][0]
      soccer_team.pop(i+1)
      #continue
    i+=1
  Upper_Case_Team = []
  trash_can_UC = ['HLV', 'CĐV' ,'BXH', 'ĐT']
  for i in range(len(soccer_team)):
    temp_str = str()
    for j in range(len(soccer_team[i][0])):
      if soccer_team[i][0][j].isupper():
        temp_str += soccer_team[i][0][j]
    soccer_team[i].append(temp_str)
    if len(temp_str)>= 1 and temp_str not in trash_can_UC:
      Upper_Case_Team.append(temp_str)
      #soccer_team[i].append(temp_str)
  #pp.pprint(Upper_Case_Team)
  for x in soccer_team:
    if '_' in x[0]:
      x[0] = x[0].replace('_', ' ')
  i = 0
  while i < len(soccer_team)-1:
    j = i+1
    while j < len(soccer_team):
      if (soccer_team[i] != soccer_team[j]):
        if (soccer_team[i][0] in soccer_team[j][0]) or (soccer_team[j][0] in soccer_team[i][0]):
          #print((soccer_team.count(soccer_team[i]), soccer_team.count(soccer_team[j])))
          if (soccer_team.count(soccer_team[i]) > soccer_team.count(soccer_team[j])):
            #c1
            t = soccer_team[j]
            t2 = soccer_team[i]
            #soccer_team = [x for x in soccer_team if x!= t ]
            soccer_team.pop(j)
            i = 0
            soccer_team.append(t2)
            break
          else :
            t = soccer_team[i]
            t2 = soccer_team[j]
            #soccer_team = [x for x in soccer_team if x!= t ]
            soccer_team.pop(i)
            soccer_team.append(t2)
            break
          i = 0
          j = i+1
          continue
      j+=1
    i+=1
  i = 0
  while i < len(soccer_team):
    j = 0
    flg = 0
    while j < len(projected_soccer_team_candidates):
      for x in projected_soccer_team_candidates[j] :
        if x in soccer_team[i][0] and x == projected_soccer_team_candidates[j][-1]:
          #print(x)
          flg = 1
      if flg == 1:
        soccer_team.append(soccer_team[i])
        projected_soccer_team_candidates.pop(j)
        break
      j+=1
    i+=1
  #RB Leipzig
  Red_Bull_Arena_count = 0
  for x in soccer_team:
    if x[0] == 'Red Bull Arena':
      Red_Bull_Arena_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'RB Leipzig':
      for k in range((Nou_Camp_count)):
        soccer_team.append(x)
      break
  #Chelsea
  Stamford_Bridge_count = 0
  for x in soccer_team:
    if x[0] == 'The Blues':
      Stamford_Bridge_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Stamford Bridge':
      Stamford_Bridge_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Chelsea':
      for k in range((Stamford_Bridge_count)):
        soccer_team.append(x)
      break
  #MU
  MU_LIST = []
  MU_COUNT = 0
  cnt_Old_Trafford = 0
  i = 0
  while i < (len(soccer_team)):
    if soccer_team[i][0] == 'Old Trafford':
      #print('OT')
      #temp = soccer_team[i]
      cnt_Old_Trafford += 1
      soccer_team.pop(i)
      i = 0
      #soccer_team = [x for x in soccer_team if x != temp]
      continue
    if soccer_team[i][2] == 'MU':
      MU_LIST.append(soccer_team[i][0])
      MU_COUNT+=1
      soccer_team.pop(i)
      i = 0
      continue
    i+=1
  if (len(MU_LIST) != 0):
    MU_occurences_count = Counter(MU_LIST)
    MU_team = MU_occurences_count.most_common(2)[0][0]
    for i in range(MU_COUNT+cnt_Old_Trafford):
      soccer_team.append([MU_team, 'B-ORG', 'MU'])
    #pp.pprint(soccer_team)
    #print(MU_team)
  #Barca
  Nou_Camp_count = 0
  for x in soccer_team:
    if x[0] == 'Nou Camp':
      Nou_Camp_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Camp Nou':
      Nou_Camp_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Barcelona':
      for k in range((Nou_Camp_count)):
        soccer_team.append(x)
      break
    if x[0] == 'Barca':
      for k in range((Nou_Camp_count)):
        soccer_team.append(x)
      break
  # Barca vs Barcelona
  i = 0
  match_count = 0
  barca_chosen = str()
  break_flg = 0
  while i < len(soccer_team):
    if break_flg == 1:
      break
    if soccer_team[i][0] == 'Barca':
      j = 0
      while j < len(soccer_team):
        #print(j)
        if soccer_team[j][0] == 'Barcelona':
          if soccer_team.count(soccer_team[i]) > soccer_team.count(soccer_team[j]):
              match_count = soccer_team.count(soccer_team[j])
              barca_chosen = soccer_team[i]
              z = (soccer_team[j])
              soccer_team = [x for x in soccer_team if x != z]
              break_flg = 1
              break
          else:
              #print(i,j,2)
              barca_chosen = soccer_team[j]
              match_count = soccer_team.count(soccer_team[i])
              z = (soccer_team[i])
              soccer_team = [x for x in soccer_team if x != z]
              break_flg = 1
              i = 0
              break
        j+=1
    i+=1
  for i in range(match_count):
    soccer_team.append(barca_chosen)
  #Leicester
  King_Power_count = 0
  for x in soccer_team:
    if x[0] == 'King Power':
      King_Power_count = soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Leicester' or 'Leicester City' :
      for k in range(King_Power_count):
        soccer_team.append(x)
      break
  #Real Madrid
  Bernabeu_count = 0
  for x in soccer_team:
    if x[0] == 'Bernabeu':
      Bernabeu_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Santiago Bernabeu':
      Bernabeu_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Santiago Bernabéu':
      Bernabeu_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Los Blancos':
      Bernabeu_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Kền kền trắng':
      Bernabeu_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'kền kền trắng':
      Bernabeu_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Real' or 'Real Madrid' :
      for k in range((Bernabeu_count)):
        soccer_team.append(x)
      break
  #Inter_Milan
  InterMilan_count =0
  for x in soccer_team:
    if x[0] == 'Nerazzurri':
      InterMilan_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Inter Milan' :
      for k in range((InterMilan_count)):
        soccer_team.append(x)
      break
  #AC and Inter Milan
  Milan_count =0
  for x in soccer_team:
    if x[0] == 'Giuseppe Meazza':
      Milan_count += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Inter Milan' :
      for k in range((Milan_count)):
        soccer_team.append(x)
      break
  for x in soccer_team:
    if x[0] == 'AC Milan' :
      for k in range((Milan_count)):
        soccer_team.append(x)
      break
  #Liverpool
  LiverpoolCount = 0
  #Merseyside
  for x in soccer_team:
    if x[0] == 'Anfield':
      LiverpoolCount += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'The Kop':
      LiverpoolCount += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'the Kop':
      LiverpoolCount += soccer_team.count(x)
      soccer_team = [z for z in soccer_team if z != x]
      break
  for x in soccer_team:
    if x[0] == 'Liverpool' :
      for k in range((LiverpoolCount)):
        soccer_team.append(x)
      break
  #Viet Nam
  for x in soccer_team:
    if 'VN' in x[2]:
      x[2] = 'VN'
  temp_list = [x for x in soccer_team]
  i = 0
  while i < len(temp_list)-1:
    j = i +1
    while j< len(temp_list):
      if temp_list[i][2] == temp_list[j][2] and temp_list[i][0] != temp_list[j][0] and len(temp_list[i][2]) > 1:
        #print(i, j)
        #print(soccer_team[i][0], soccer_team[j][0])
        if temp_list.count(temp_list[i]) > temp_list.count(temp_list[j]) :
          t = temp_list[j]
          cnt = temp_list.count(temp_list[j])
          for k in range(cnt):
            temp_list.append(temp_list[i])
          temp_list = [x for x in temp_list if x != t]
        else :
          t = temp_list[i]
          cnt = temp_list.count(temp_list[i])
          for k in range(cnt):
            temp_list.append(temp_list[j])
          temp_list = [x for x in temp_list if x != t]
      j+=1
    i+=1
  #temp_list
  #soccer_team
  i = 0
  while i < len(temp_list)-1:
    j = i+1
    while j< len(temp_list) -1:
      if temp_list[i] != temp_list[j] and len(temp_list[i][0]) == len(temp_list[j][0]):
        if temp_list[i][0].lower() == temp_list[j][0].lower():
          if temp_list.count(temp_list[i]) > temp_list.count(temp_list[j]):
            cnt = temp_list.count(temp_list[j])
            x = temp_list[j]
            temp_list = [z for z in temp_list if z != x]
            for k in range(cnt):
              temp_list.append(temp_list[i])
            i = 0
            break
          else:
            cnt = temp_list.count(temp_list[i])
            x = temp_list[i]
            temp_list = [z for z in temp_list if z != x]
            for k in range(cnt):
              temp_list.append(temp_list[j])
            i = 0
            break
      j+=1
    i+=1
  # Given list
  listA = []
  for x in temp_list:
    listA.append(tuple(x))
  team_occurence_count = Counter(listA)
  listA = team_occurence_count.most_common()
  #print("Given List:\n",listA)
  team1_candidates = []
  x = listA[0][1]
  team1_candidates.append(listA[0])
  for i in range(1,len(listA)):
    if x == listA[i][1]:
      team1_candidates.append(listA[i])
  #print(team1_candidates)
  if len(team1_candidates) == 1:
    team1 = listA[0][0][0]
    listA.pop(0)
    team2_candidates = []
    team2_candidates.append(listA[0])
    x = listA[0][1]
    for i in range(1,len(listA)):
      if x == listA[i][1]:
        team2_candidates.append(listA[i])
    #print(team2_candidates)
    if len(team2_candidates) == 1:
      team2 = team2_candidates[0][0][0]
    else:
      for i in range(len(team2_candidates)):
        if team2_candidates[i][0][1] == 'B-ORG':
          #print('yana')
          team2 = team2_candidates[i][0][0]
          break
        if i == len(team1_candidates) - 1:
          #print('myanmar')
          team2 = team2_candidates[1][0][0]
  elif len(team1_candidates) == 2:
    team1 = team1_candidates[0][0][0]
    team2 = team1_candidates[1][0][0]
  else :
    flg_d = 0
    for i in range(len(team1_candidates)):
      if flg_d == 1:
        break
      if team1_candidates[i][0][1] == 'B-ORG':
        team1 = team1_candidates[i][0][0]
        #print(i)
        for j in range(i+1,len(team1_candidates)):
          if team1_candidates[j][0][1] == 'B-ORG':
            team2 = team1_candidates[j][0][0]
            flg_d = 1
            break
          if j == len(team1_candidates)-1:
            team2 = team1_candidates[i+1][0][0]
        break
      if i == len(team1_candidates) - 1:
        team1 = team1_candidates[0][0][0]
        team2 = team1_candidates[1][0][0]
  #print(team1,team2)
  team1 = team1.replace('_',' ')
  team2 = team2.replace('_',' ')
  #player names of score list with time
  score_list_team1 = []
  score_list_team2 = []
  #Ghi bàn ' '
  find1a = clean_text.find("Ghi bàn ")
  if find1a != -1:
    #1st string
    i = find1a+8
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    #The next one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    #print(score_list_team1)
  find1b = clean_text.find("Ghi bàn ",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+8
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #BÀN THẮNG.
  find1a = clean_text.find("BÀN THẮNG.")
  if find1a != -1:
    #1st string
    i = find1a+10
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    #The next one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    #print(score_list_team1)
  find1b = clean_text.find("BÀN THẮNG.",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+10
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #Ghi bàn.
  find1a = clean_text.find("Ghi bàn.")
  if find1a != -1:
    #1st string
    i = find1a+8
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    #The next one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    #print(score_list_team1)
  find1b = clean_text.find("Ghi bàn.",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+8
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if (clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+') and colon_flg == 1:
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #Ghi bàn:
  find1a = clean_text.find("Ghi bàn:")
  if find1a != -1:
    #1st string
    i = find1a+8
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
    #The next one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
  find1b = clean_text.find("Ghi bàn:",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+8
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #Cầu thủ ghi bàn:
  find1a = clean_text.find("Cầu thủ ghi bàn:")
  if find1a != -1:
    i = find1a+16
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
  find1b = clean_text.find("Cầu thủ ghi bàn",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+16
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #Scorer:
  find1a = clean_text.find("Scorer:")
  if find1a != -1:
    i = find1a+7
    if clean_text[i] != '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
    #The next one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
  find1b = clean_text.find("Scorer:",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+7
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #Bàn thắng:
  find1a = clean_text.find("Bàn thắng:")
  if find1a != -1:
    #print('wtf 1')
    i = find1a+10
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
    #The second one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
  find1b = clean_text.find("Bàn thắng:",find1a+2)
  #print(find1b)
  if find1b != -1 :
    #print('wtf 2')
    i = find1b+10
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #BÀN THẮNG:
  find1a = clean_text.find("BÀN THẮNG:")
  if find1a != -1 :
    #1st string
    i = find1a+10
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
    #The next one
    i+=1
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    while clean_text[i]!= '.':
      #O.G processed
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str+=clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team1.append(name_str)
    """
  find1b = clean_text.find("BÀN THẮNG:",find1a+2)
  #print(find1b)
  if find1b != -1:
    i = find1b+10
    if clean_text[i] == '.':
      i+=1
    colon_flg = 0
    num_flg = 0
    name_str = str()
    #flg_paren = 0
    while clean_text[i]!= '.':
      #O.G processed
      #name_str+=clean_text[i]
      if clean_text[i+1] == '.' and clean_text[i] == 'O':
        name_str += clean_text[i]
        i+=2
        continue
      if clean_text[i] == ':':
        name_str = str()
        colon_flg = 1
        i+=2
        continue
      #if clean_text[i] == ' '
      if clean_text[i].isalnum() or clean_text[i] == ' ' or clean_text[i] == '(' or clean_text[i] == ')' or clean_text[i] == '+':
        name_str +=clean_text[i]
        i+=1
        continue
      if clean_text[i] == '(':
        #flg_paren = 1
        i+=1
        continue
      if clean_text[i] == ')':
        #flg_paren = 0
        i+=1
        continue
      #if clean_text[i].isalnum or clean_text[i].
      i+=1
    score_list_team2.append(name_str)
  #print(score_list_team1, score_list_team2)
  final_team1_sl = []
  team1_sl = []
  temp_str = str()
  if len(score_list_team1) == 2:
    score_list_team2.append(score_list_team1[1])
    score_list_team1.pop(1)
    pass
  if len(score_list_team1) == 1:
    score_list_team1[0] =score_list_team1[0].replace('OG','')
    #print(score_list_team1)
    score_list_team1[0]+=' P'
    i = 0
    if score_list_team1[0][i] == ' ':
      i+=1
    num_flg = 0
    while i < len(score_list_team1[0]):
      if score_list_team1[0][i].isalnum() or score_list_team1[0][i] == '-' or score_list_team1[0][i] == ' ' or score_list_team1[0][i] == '+':
        if score_list_team1[0][i] == ' ' and score_list_team1[0][i+1].isalpha() and score_list_team1[0][i+1].isupper() and num_flg ==1:
          #print(i)
          num_flg = 0
          team1_sl.append(temp_str)
          temp_str = str()
          i+=1
          continue
        if score_list_team1[0][i].isnumeric():
          num_flg = 1
        temp_str+=score_list_team1[0][i]
        i+=1
        continue
      i+=1
      continue
    team1_sl = [x.split() for x in team1_sl]
    final_team1_sl = []
    i = 0
    while i < len(team1_sl):
      j = 0
      temp_list = []
      while j < len(team1_sl[i]):
        if team1_sl[i][j][0].isupper() or team1_sl[i][j][0].isnumeric():
          temp_list.append(team1_sl[i][j])
          j+=1
          continue
        j+=1
      final_team1_sl.append(temp_list)
      i+=1
    i = 0
    while i < len(final_team1_sl):
      j = 0
      while j < len(final_team1_sl[i]):
        if final_team1_sl[i][j][0].isupper() and final_team1_sl[i][j+1][0].isupper():
          final_team1_sl[i][j] += ' ' + final_team1_sl[i][j+1]
          final_team1_sl[i].pop(j+1)
          j = 0
          continue
        j+=1
        continue
      i+=1
  final_team2_sl = []
  team2_sl = []
  if len(score_list_team2) == 1:
    score_list_team2[0] =score_list_team2[0].replace('OG','')
    temp_str = str()
    score_list_team2[0]+=' P'
    i = 0
    if score_list_team2[0][i] == ' ':
      i+=1
    num_flg = 0
    while i < len(score_list_team2[0]):
      if score_list_team2[0][i].isalnum() or score_list_team2[0][i] == '-' or score_list_team2[0][i] == ' ' or score_list_team2[0][i] == '+':
        if score_list_team2[0][i] == ' ' and score_list_team2[0][i+1].isalpha() and score_list_team2[0][i+1].isupper() and num_flg ==1:
          #print(i)
          num_flg = 0
          team2_sl.append(temp_str)
          temp_str = str()
          i+=1
          continue
        if score_list_team2[0][i].isnumeric():
          num_flg = 1
        temp_str+=score_list_team2[0][i]
        i+=1
        continue
      i+=1
      continue
    team2_sl = [x.split() for x in team2_sl]
    final_team2_sl = []
    i = 0
    while i < len(team2_sl):
      j = 0
      temp_list = []
      while j < len(team2_sl[i]):
        if team2_sl[i][j][0].isupper() or team2_sl[i][j][0].isnumeric():
          temp_list.append(team2_sl[i][j])
          j+=1
          continue
        j+=1
      final_team2_sl.append(temp_list)
      i+=1
    i = 0
    while i < len(final_team2_sl):
      j = 0
      while j < len(final_team2_sl[i]):
        if final_team2_sl[i][j][0].isupper() and final_team2_sl[i][j+1][0].isupper():
          final_team2_sl[i][j] += ' ' + final_team2_sl[i][j+1]
          final_team2_sl[i].pop(j+1)
          j = 0
          continue
        j+=1
        continue
      i+=1
  #print(final_team1_sl,final_team2_sl)
  d = {"test_id": "%d"%(test_id), "match_summary": {"players": {"team1": "%s"%team1, "team2": "%s"%team2}, "score_board": {"score1": "%s"%final_score_1, "score2": "%s"%final_score_2}, "score_list": [], "card_list": [{"player_name": "", "time": "", "team": ""}], "substitution_list": [{"player_in": "", "time": "", "player_out": ""}]}}
  #According to the order of team names
  if len(final_team1_sl) !=0:
    for i in range(len(final_team1_sl)):
      for j in range(len(final_team1_sl[i])-1):
        d['match_summary']['score_list'].append({"player_name": "%s"%final_team1_sl[i][0], "time": "%s"%final_team1_sl[i][j+1], "team": "%s"%team1})
  if len(final_team2_sl) !=0:
    for i in range(len(final_team2_sl)):
      for j in range(len(final_team2_sl[i])-1):
        d['match_summary']['score_list'].append({"player_name": "%s"%final_team2_sl[i][0], "time": "%s"%final_team2_sl[i][j+1], "team": "%s"%team2})
  list_dict.append(d)
with open('submission.jsonl', 'w') as out_file:
    for i in range(len(list_dict)):
      out_file.write(json.dumps(list_dict[i],ensure_ascii=False))
      out_file.write("\n")