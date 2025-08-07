# ✨ 추천 서버 (Recommendation Server)
<br/>
사용자의 실시간 행동 로그를 기반으로 개인화된 콘텐츠를 추천하기 위한 유저 벡터 연산과 가중치 업데이트를 하는 서버입니다.
Low latency추천 응답과 유연한 추천 파이프라인 구성을 목표로 합니다.

<br/>
<br/>

## 🔁 데이터 흐름 예시
<br/>

사용자 행동 발생 시, 추천 시스템은 다음과 같은 흐름으로 동작합니다:

```mermaid
sequenceDiagram
    participant Client
    participant API_Server as Spring Boot
    participant MQ as RabbitMQ
    participant RecoServer as 추천 서버 (FastAPI)
    participant Mongo as MongoDB
    participant Redis as Redis

    Client->>API_Server: 클릭 / 좋아요 등 행동 발생
    API_Server-->>MQ: 행동 메시지 전송 (userId, contentId 등)
    MQ-->>RecoServer: 메시지 소비 (비동기)
    Mongo->>RecoServer: 유저 장르 가중치 조회 
    RecoServer->>Mongo: 장르별 유저 가중치 업데이트
    RecoServer->>Redis: 계산된 유저 벡터 캐싱
```

>💡 사용자 벡터는 Redis에 캐시되어 있으며, 추천 요청 시 PGVector의 콘텐츠 벡터와의 유사도 연산으로 빠르게 추천 결과를 반환합니다.

<br/>

##


## 🛠 기술 스택

<p align="left">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-0db7ed?style=flat&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white"/>
  <img src ="https://img.shields.io/badge/-rabbitmq-%23FF6600?style=flat&logo=rabbitmq&logoColor=white"/>
</p>
