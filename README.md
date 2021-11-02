# discord_auction_bot

## 1. 프로젝트 개요

1. 프로젝트 내용

  * dicord open API를 이용한 디스코드 봇 프로젝트
  
  * 사용자는 해당 봇을 이용해 게임 아이템 물품을 등록, 입찰할 수 있다.
  
  
## 2. 명령어

* .목록

  * 현재 등록된 물품 목록을 보여준다.

  * 출력 예시

    ```markdown
    -홍길동-
    포도
    딸기
    블루베리
    
    -김철수-
    참외 - 홍길동 입찰희망
    수박 - 김영희 입찰희망
    
    -김영희-
    메론
    
    -김가람-
    토마토 - 김철수, 홍길동 입찰희망
    감자
    ```

* .초기화

  * 목록을 초기화한다.

  * 출력 예시

    ```markdown
    '<아이디>'님이 목록을 초기화하였습니다.
    ```
    
* .등록 <물품이름>

  * 해당 물품을 등록한다.

  * 출력 예시

    ```markdown
    '<아이디>'님이 물품을 등록하였습니다: <물품이름>
    ```

* .입찰 <등록자 아이디> <물품 이름>

  * 해당 등록자의 물품에 입찰한다.

  * 출력 예시

    ```markdown
    '<아이디>'님이 입찰하였습니다: <등록자 아이디> - <물품 이름>
    ```

* .등록삭제 <물품이름>

  * 해당 등록물품을 삭제한다.

  * 출력 예시

    ```markdown
    '<아이디>'님이 등록된 물품을 삭제하였습니다: <물품이름>
    ```

* .입찰삭제 <등록자 아이디> <물품 이름>

  * 해당 입찰을 취소한다.

  * 출력 예시

    ```markdown
    '<아이디>'님이 입찰을 취소하였습니다: <등록자 아이디> - <물품 이름>
    ```



    

