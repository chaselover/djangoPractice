# Django ORM 성능 최적화 N + 1 Problem

## ORM이란 

* Object Relation Mapper

* 객체와 관계형 data를 자동으로 매핑해주는 것.
* 객체를 통해 간접적으로 database data를 다룬다.

<br>

## ORM의 장점

* `객체지향`적인 코드로 인해 더 직관적이고 `비즈니스 로직`에 더 집중 할 수 있게 해준다.

* 재사용 및 유지보수 용이
* DBMS에 대한 종속성이 줄어든다. ( MySQL -> PostgreSQL로 바꿔도 금방 테이블 생성 가능.)

<br>

## ORM의 단점

* ORM으로만 완벽한 서비스를 구현할 수 없다.
* 프로시저가 많은 시스템에선 ORM의 객체 지향적인 장점을 활용하기 어렵다.
* 프로젝트의 복잡성이 크면 구현하는 난이도가 상승한다.

<br>

## N + 1 Problem

* django ORM은 Lazy-Loading 방식
* ORM에서 명령을 실행할 때마다 데이터베이스에서 데이터를 가져오는 것이 아니라 
* 모든 명령 처리가 끝나고 실제로 데이터를 불러와야 할 시점이 왔을 때 DB에 쿼리를 실행하는 방식.

```python
# 1. 
# 아직 쿼리를 보내지 않았다.
items = item.objects.all()

for item in items:
	# 호출 시점에서 쿼리를 날린다.
	# 문제는 서브 item 즉 Join이 필요한 데이터는 1번 호출이면 끝날 쿼리를
	# N번 만큼 호출 하게 된다.
	print(item.sub_item)
    
    
# 2 장점은 매 단계 쿼리를 날리지 않아 쿼리 요청을 최소화 할 수 있다든 것.
user = User.objects.all()
a = user.filter(first_name='a')  # 아직 DB에서 데이터를 가져오지않음
order_a = a.order_by('id')       # 아직 DB에서 데이터를 가져오지않음
b = user.get(id=1)
parent = b.parent.name           # parent 를 가져오는 쿼리를 더 보냄
```

* N + 1 문제는 쿼리 1번으로 N건의 data를 가져왔는데 원하는 데이터를 얻기 위해 N건의 데이터를 더 반복해 2차적으로 쿼리를 수행하게 되는 문제 

* Eager-Loading으로 사전에 쓸 데이터를 포함해 쿼리를 날리기 때문에 비효율적으로 늘어나는 쿼리를 방지할 수 있다. ( lazy-loading은 쿼리 요청을 할 떄 어떤 데이터를 필요로 하는지 모르기에 하나 하나 쿼리를 보내는 것.)

```python
#1
# select_related로 데이터를 바로 가져왔다. (Join)
items = item.objects.select_related('sub_item').all()

for item in items:
	# 이미 데이터가 있기 때문에 그냥 순회를 돈다.
	# 1번의 쿼리로 처리가 되었다.
	print(item.sub_item)

#2
user = User.objects.all()
parent = user.prefetch_related('parent')  # parent를 가져오는 쿼리를 사전에 날림
```

1. select_related : foreign-key, one-to-one처럼 single-valued relationships에서만 사용이 가능하다. SQL의 JOIN을 사용하는 방법.
2. prefetch_related : foreign-key, one-to-one 뿐만 아니라 many-to-many, many-to-one 등 모든 relationships에서 사용 가능하다. SQL의 WHERE ... IN 구문을 사용하는 방법이다.

* 위와 같은 방식은 필요한 데이터를 얻기 위해 계속 쿼리를 보내는 것이 아니라 local data cache에 가져온 데이터를 보관했다가 필요할 때 즉각적으로 제공함으로써 쿼리 요청을 DB에 보내는 것보다 빠르다.

<br>

> 동일하게 Serializer에 Serializer가 중첩된 경우 증 Nested Serializer를 사용하는 것이 성능 저하의 원인 중 하나.

```python
class UserSerializer(serializer.ModelSerializer):
    estimates = EstimateSerializer(many=True, read_only=True)
```

* User가 많아질수록 쿼리수도 많아져 성능은 최악으로 간다.

<br>

<br>

## Reference

* https://jisun-rea.tistory.com/entry/Django-ORM-QuerySet-%EC%88%98%EC%A0%95%EC%9D%84-%ED%86%B5%ED%95%B4-%EC%84%B1%EB%8A%A5-%ED%96%A5%EC%83%81%EC%8B%9C%ED%82%A4%EA%B8%B0-SQL-Queries-%EC%A4%91%EB%B3%B5-%EC%A4%84%EC%9D%B4%EA%B8%B0-selectrelated-prefetchrelated
* https://velog.io/@kim6515516/npuls

<br>

## 관련 추후 공부해야 할 포스팅

* https://americanopeople.tistory.com/323
* https://blog.naver.com/wlsdml1103/221837463679