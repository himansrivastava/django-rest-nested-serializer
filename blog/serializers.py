from rest_framework import serializers
from .models import User, Comment


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ("id", "email", "username", "comment")

    def update(self, instance, validated_data):
        comment_data = validated_data.pop("comment")

        # Saving the user information
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()

        print(instance.id)
        existing_data = {
            comment.id: comment for comment in Comment.objects.filter(user=instance.id)
        }
        # existing_data stores the current ids of the child model in the database
        current_data = []
        # current_data stores the ids of the child model in the incoming data

        # Perform creations and updates in the comment model
        for comment in comment_data:
            comment_id = comment.get("id", None)
            if comment_id is None:
                Comment.objects.create(**comment)
            else:
                current_data.append(comment_id)
                # current_data creates a list of old records in the incoming data
                # This list of old records in the incoming data will be cross checked
                # with the records currently present in the database.

                Comment.objects.filter(id=comment_id).update(**comment)

        # Perform deletions
        # The records which are currently present in the database but are not present
        # in the incoming data should be deleted.
        print(current_data)
        for comment_id, comment in existing_data.items():
            if comment_id not in current_data:
                comment.delete()

        return instance


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("id", "email", "username")


# class CommentSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Comment
#         fields = "__all__"

#     def create(self, validated_data):
#         # print(validated_data)
#         user_data = validated_data.pop("user")
#         user_obj = User.objects.create(**user_data)
#         # print("user obj")
#         # print(user_obj.id)
#         # print(validated_data)
#         comment = Comment.objects.create(user=user_obj, **validated_data)
#         return comment

#     def update(self, instance, validated_data):
#         print("Instance:")
#         print(instance)
#         print(validated_data)
#         user_data = validated_data.pop("user")
#         user = instance.user
#         # print("user")
#         # print(user)
#         # print(user_data["email"])
#         user.email = user_data["email"]
#         user.username = user_data["username"]
#         user.save()
#         instance.content = validated_data.get("content", instance.content)
#         instance.created = validated_data.get("created", instance.created)
#         instance.save()
#         return instance
