from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import data_conversion as dc
import os

mecab = dc.Mecab(dicpath="C:\\mecab\\mecab-ko-dic")


# kkk.train 의 클래스 str 값에 따라 0, 1, 2, 3을 반환 / tfidf matrix의 문서 분류의 인덱스를 위해 필요함 
def get_intent_number(intent_str):
    if intent_str == "상품 소개":
        return 0
    if intent_str == "지점 안내":
        return 1
    if intent_str == "고객 상담":
        return 2
    if intent_str == "상품 추천":
        return 3


# kkk.train 의 질문을 형태소 분류하고, 나뉜 각 단어들에 대한 tf-idf 값 구현
def make_tfidf_matrix():
    pf = open('./data/kkk.train', 'r', encoding='utf-8')
    corpus_by_intent = ["" for _ in range(4)]       # 문장 뭉치의 갯수는 검색 모델 의도 수 (4)
    list_in_corpus = [[] for _ in range(4)]
    text = pf.read().split('\n')
    
    # kkk.train 을 한 라인 씩 읽어 ',' 뒤의 값은 클래스 의도에 대한 숫자로 변환, 앞의 값은 형태소 분석하여 동사, 명사를 추출 후 리스트로 저장
    for line in text:       
        splited_line = [string.strip() for string in line.split(',')]
        intent_num = get_intent_number(splited_line[1])
        line_pos_list = mecab.pos(splited_line[0])

        for line_pos in line_pos_list:
            if line_pos[1][0] == "N" or line_pos[1][0] == "V":  # 형태소가 명사, 동사일 경우
                list_in_corpus[intent_num].append(line_pos[0])

    # 정제된 단어의 list 를 join 하여 하나의 corpus (string) 으로 변환
    for num in range(4):
        corpus_by_intent[num] = ' '.join(list_in_corpus[num])

    # tf-idf matrix 를 생성
    vect = TfidfVectorizer()
    tfidf_matrix = vect.fit_transform(corpus_by_intent)
    
    # DataFrame 에 넣어 저장
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=vect.get_feature_names())
    pd.set_option('display.max_columns', 115)
    df.to_csv('./data/tfidfMatrix.csv', header=True, index=False, encoding='utf-8')


def load_tfidf_matrix():    # 경로 안의 csv 파일을 읽어 DataFrame 생성 후 반환
    df = pd.DataFrame()
    if os.path.exists('./data/tfidfMatrix.csv'):
        df = pd.read_csv('./data/tfidfMatrix.csv')
        return df
    else:
        make_tfidf_matrix()
        df = pd.read_csv('./data/tfidfMatrix.csv')
        return df



def get_tfidf_result(input_msg, df):    # 문장과 dataframe 을 입력 받아 문장 형태소들의 tf-idf 값을 조회 후 그 값을 반환
    pos_result = set()
    pos_list = mecab.pos(input_msg)
    for pos in pos_list:
        if pos[1][0] == "N" or pos[1][0] == "V":  # 형태소가 명사, 동사일 경우
            pos_result.add(pos[0])
            
    tfidf_result = [0 for _ in range(4)]

    for pos_item in pos_result:
        if pos_item in TFIDF_MATRIX.columns:
            for num in range(4):
                tfidf_result[num] = tfidf_result[num] + df[pos_item].values[num]

    return tfidf_result


def is_unknown(msg, df):
    tfidf_list = get_tfidf_result(msg, df)
    if all([c < 0.18 for c in tfidf_list]): # 0.2 는 실험적인 값
        return True
    else:
        return False


TFIDF_MATRIX = load_tfidf_matrix()


# make_tfidf_matrix()
# print(TFIDF_MATRIX)
# print(get_tfidf_result("대출", TFIDF_MATRIX))