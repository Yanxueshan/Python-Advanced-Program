'''
    模拟Django的ORM实现
'''
import numbers
import pymysql


def judge_int(value):
    if not isinstance(value, numbers.Integral):
        raise ValueError("value must input int")
    if value < 0:
        raise ValueError("value input positive number")


def judge_str(value):
    if not isinstance(value, str):
        raise ValueError("please input str")


class Field:
    pass


class CharField(Field):
    def __init__(self, db_column, min_length=0, max_length=0):
        self._value = ""
        self.db_column = db_column

        self.min_length = min_length
        self.max_length = max_length

        judge_int(self.min_length)
        judge_int(self.max_length)
        if self.min_length > self.max_length:
            raise ValueError("max_length must great than min_length")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        judge_str(value)
        if len(value) < self.min_length or len(value) > self.max_length:
            raise ValueError("value length must between min_length and max_length")
        self._value = value


class IntField(Field):
    def __init__(self, db_column, min_value=0, max_value=100):
        self._value = 0
        self.db_column = db_column

        self.max_value = max_value
        self.min_value = min_value

        judge_int(self.min_value)
        judge_int(self.max_value)
        if self.min_value > self.max_value:
            raise ValueError("max_value must great than min_value")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        judge_int(value)
        if value < self.min_value or value > self.max_value:
            raise ValueError("value must between min_value and max_value")
        self._value = value


class UserMetaClass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs, **kwargs)
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        db_table = name.lower()
        _meta = {}
        attrs_meta = attrs.get("Meta", None)
        if attrs_meta is not None:
            table = getattr(attrs_meta, "db_table", None)
            if table is not None:
                db_table = table
        
        _meta["db_table"] = db_table

        attrs['fields'] = fields
        attrs['_meta'] = _meta
        del attrs['Meta']

        return super().__new__(cls, name, bases, attrs, **kwargs)


class BaseModel(metaclass=UserMetaClass):
    def __init__(self, *args, **kwargs):
        self.connect = pymysql.Connect(host="localhost", port=3306, user="root", passwd="root", db="test")
        self.cursor = self.connect.cursor()

        for key, value in kwargs:
            setattr(self, key, value)
        return super().__init__()
    
    def save(self):
        fields = []
        values = []
        db_table = self._meta["db_table"]
        for key, value in self.fields.items():
            db_column = getattr(value, "db_column")
            if db_column is None:
                db_column = key.lower()
            fields.append(db_column)
            value = getattr(value, "_value")
            values.append(str(value))
        
        value = "%s," * len(values)
        value = value[:-1]
        
        insert_sql = "insert into {db_table}({fields}) values({value})".format(db_table=db_table, fields=",".join(fields), value=value)

        self.cursor.execute(insert_sql, values)
        self.connect.commit()
        print('insert sucess')
        self.cursor.close()
        self.connect.close()


class User(BaseModel):
    name = CharField(db_column="name", max_length=10)
    age = IntField(db_column="age", min_value=0, max_value=100)

    class Meta:
        db_table = "user"


user = User()
user.name = 'shiyue'
user.age = 10
user.save()
