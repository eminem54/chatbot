# Chatbot

---
### 새마을 금고 연계 졸업 프로젝트(4인)

### 검색모델과 생성모델을 결합한 금융 상담 챗봇


---
<img src="https://user-images.githubusercontent.com/40411705/71540134-e8ba4000-2989-11ea-83e8-954cc7e8c75b.png" />

-  Entity 추출 - 사용자의 질문에서 핵심 단어를 추출한다. 
-  TF-IDF - 훈련 데이터로 얻은 TF-IDF를 적용하여 생성 모델에 대한 의도를 추출
-  Intent 추출 - 딥러닝 모델 Feed Forward Neural Network 형태의 모델로 Multi Classification 기능을 구현한다. 이를 통해 질문에서 사용자의 의도를 추출한다.
-  Slot Filling - 대답을 하기 위한 핵심단어와 의도가 준비되면 그 데이터를 토대로 적절한 답변을 Database에서 가져온다.
-  생성모델 - Recurrent Neural Network 중 하나인 Seq2Seq 모델을 이용하여 적절한 일상 대화를 학습 시켜 답변을 생성한다.
- 코사인 유사도 - 코사인 유사도는 두 벡터 간의 코사인 각도를 이용하여 구할 수 있는 두 벡터의 유사도를 의미하며, 유사도 값을 가지는 범위는 -1 이상 1 이하의 값을 가지며 값이 1에 가까울수록 유사도가 높다고 판단

---
### 기술 스택
- Keras 2.2.4
  - Tensorflow 1.8.0
- Flask 1.0.2
- MongoDB
- Mecab
