import graphene
from graphene_django import DjangoObjectType
from main.models import Category, Post


class CategoryModelType(DjangoObjectType):
    class Meta:
        model = Category


#  Работает как serializer
class PostModelType(DjangoObjectType):
    class Meta:
        model = Post

# Работает как viewset
class Query(graphene.ObjectType):
    category_model = graphene.List(CategoryModelType)
    post_model = graphene.List(PostModelType)

    def resolve_category_model(self, info):
        return Category.objects.all()
    
    def resolve_post_model(self, info):
        return Post.objects.all()
    
#---------------------------------------------------------------------------
  
class CreateCategory(graphene.Mutation):   # POST  - чтобы создать объекты
    class Arguments:
        newname = graphene.String()

    category = graphene.Field(CategoryModelType)

    def mutate(self, info, newname):
        category = Category.objects.create(name=newname)
        return CreateCategory(category=category)
    
class CreatePost(graphene.Mutation):
    class Arguments:
        image = graphene.String()
        title = graphene.String()
        description = graphene.String()
        category = graphene.Int()
        location = graphene.String()
        
    post = graphene.Field(PostModelType)

    def mutate(self, info, image,title, description, category,location):
        post = Post.objects.create(image=image ,title=title, description= description, category= Category.objects.get(id=category),location=location)
        return CreatePost(post=post)
              
#--------------------------------------------------------------------    
class UpdateCategory(graphene.Mutation): # PUT  -  чтобы изменить что-то
    class Arguments:
        id = graphene.ID(required=True)
        newname = graphene.String()   

    category = graphene.Field(CategoryModelType)

    def mutate(self, info, id, newname):
        category = Category.objects.get(id=id)
        if newname:
            category.name = newname
            
        category.save()    
        return UpdateCategory(category=category)
    
class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        image = graphene.String()
        title = graphene.String()
        description = graphene.String()
        category = graphene.Int()
        location = graphene.String()

    post = graphene.Field(PostModelType)

    def mutate(self, info, id, image=None,title=None, description=None, category=None,location=None):
        post = Post.objects.get(id=id)    
        
        if image:
            post.image = image
        if title:
            post.title = title
        if description:
            post.description = description
        if category:
            post.category = category
        if location:
            post.location = location

        post.save()
        return UpdatePost(post=post)
        
#------------------------------------------------------------------
class DeleteCategory(graphene.Mutation):  # DELETE
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()    # False

    def mutate(self, info, id):
        category  = Category.objects.get(id=id)
        category.delete()
        return DeleteCategory(success=True)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean() # False

    def mutate(self, info, id):
        post = Post.objects.get(id=id)
        post.delete()
        return DeletePost(success=True)          

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()     

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    

 # Работает как routers
schema = graphene.Schema(query=Query, mutation=Mutation)
