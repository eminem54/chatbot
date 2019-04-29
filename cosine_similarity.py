from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import csv

from sklearn.metrics.pairwise import linear_kernel
class Similarity:
    #유사한 문장 찾기 위해서 csv 파일을 만든다.
    def get_csv_writer(callStr,filename,rows,delimiter):
        with open('dataMake.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
            fieldnames = ['index', 'answer','question']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=delimiter)
            writer.writeheader()
            idx=0
            writer.writerow(({'index':0,'answer':'','question':callStr}))
            for row in rows:
                idx=idx+1
                writer.writerow({'index':idx,'answer':row[1],'question':row[0]})

    #훈련 데이터 파일을 불러온다.
    def get_csv_reader(filename,delimiter):
        reader=[]
        f=open(filename,'r',encoding='utf-8-sig')
        rdr=csv.reader(f)
        for line in rdr:
            reader.append(line)
        return list(reader)

    #코사인 유사도를 사용해서 유사한 문장과 의도를 가져온다
    def get_similarity(index,data,cosine_sim,indices):
        # 선택한 문장의 인덱스로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 문장을 가지고 연산할 수 있습니다.
        idx = indices[index]

        # 모든 문장에 대해서 해당 문장과의 유사도를 구합니다.
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 유사도에 따라 정렬
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 가장 유사한 문장을 저장.
        sim_scores = sim_scores[1:11]

        # 가장 유사한 문장의 인덱스를 받는다.
        content_indices = [i[0] for i in sim_scores]

        return data['answer'].iloc[content_indices],data['question'].iloc[content_indices]


    def get_contents(self,call_str):
        '''
        고객에게 문장을 받으면 훈련 데이터를 읽고
        유사도를 추측하기위한 csv파일을 만든다.
        '''
        data = []
        data = self.get_csv_reader('faq_data0.csv', ",")
        self.get_csv_writer(call_str, 'dataMake.csv', data, ",")

        """
        전처리 과정 학습시킬 데이터들을 tf-idf를 이용해서 행렬화한다.
        """
        # 데이터를 읽어온다.
        data = pd.read_csv('dataMake.csv', low_memory=False)
        data = data.head(300)


        tfidf = TfidfVectorizer()
        data['question'] = data['question'].fillna('')
        tfidf_matrix = tfidf.fit_transform(data['question'])

        # 코사인 유사도를 사용하면 바로 문서의 유사도를 구할수 있다.
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        indices = pd.Series(data.index, index=data['index']).drop_duplicates()
        intent,content=self.get_similarity(0,data,cosine_sim,indices)
        return intent,content


    #고객 요청과 유사한 문장,의도 추출
    call_str='대출 할래'
    intent,content=get_contents(call_str)
    print('유사한 의도 = '+intent+'  //      유사한 문장 = '+content)