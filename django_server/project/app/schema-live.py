import graphene
import graphene_django
from django.contrib.auth.backends import UserModel
from django.db.models import Avg

from .models import Book, HasRead


class UserType(graphene_django.DjangoObjectType):
    is_admin = graphene.Boolean()
    avg_rating = graphene.Float()

    def resolve_is_admin(self, info):
        return self.is_staff

    def resolve_avg_rating(self, info):
        q = self.books_read.aggregate(Avg('rating'))
        return q['rating__avg'] 

    class Meta:
        model = UserModel
        only_fields = ('id', 'username', 'books_read')

class BookType(graphene_django.DjangoObjectType):
    class Meta:
        model = Book

class HasReadType(graphene_django.DjangoObjectType):
    class Meta:
        model = HasRead

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    books = graphene.List(BookType)

    def resolve_users(self, info):
        return UserModel.objects.all()

    def resolve_books(self, info):
        return Book.objects.all()

schema = graphene.Schema(query=Query)