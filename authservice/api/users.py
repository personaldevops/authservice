from dataclasses import dataclass, field
from abstractions.mongo_abstractions.operations import MongoFilter
from abstractions.mongo_abstractions.operations import MongoFindFilter
from abstractions.mongo_abstractions.mongo_query_builder import MongoQueryBuilder
from abstractions.enums.mongo import MongoPredicates
from abstractions.enums.mongo import MongoActions
from authservice.models.auth_request_models import UserSignIn, UserSignUp


@dataclass
class SignUp:
    user: UserSignUp

    @property
    def exists(self) -> bool:
        email = self.user.email
        query_filter = MongoFilter(
            attribute='email', predicate=MongoPredicates.EqualTo, value=email)
        query = MongoFindFilter()
        query.add_filter(filter=query_filter)
        db_find = MongoQueryBuilder(schema='authorization', collection='signup_info', action=MongoActions.Find,
                                    filters=query).execute_query()
        if len(db_find) > 0:
            return True
        return False

    def write(self):
        db_entry = {"email": self.user.email, "password": self.user.password,
                    "first_name": self.user.first_name, "last_name": self.user.last_name}
        MongoQueryBuilder(schema='authorization', collection='signup_info',
                          action=MongoActions.Insert, data=db_entry).execute_query()


@dataclass
class SignIn:
    user: UserSignIn
    data: dict = field(default_factory=dict)

    @property
    def exists(self) -> bool:
        email = self.user.email
        query_filter = MongoFilter(
            attribute='email', predicate=MongoPredicates.EqualTo, value=email)
        query = MongoFindFilter()
        query.add_filter(filter=query_filter)
        db_find = MongoQueryBuilder(schema='authorization', collection='signup_info', action=MongoActions.Find,
                                    filters=query).execute_query()
        if len(db_find) == 0:
            return False
        self.data = db_find[0]
        return True

    @property
    def authenticated(self) -> bool:
        if self.data['password'] == self.user.password:
            return True
        return False
