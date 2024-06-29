from django.db import models
from django.contrib.auth.models import User
 
# Create your models here.

class Folder(models.Model):
    name = models.CharField(
        blank=False,
        help_text="Enter the name of the folder",
        max_length=255,
        null=False,
        primary_key=False,
        unique=False,
        verbose_name="Folder Name",
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        help_text="Select the parent directory. Leave empty if this is a root directory.",
        null=True,
        on_delete=models.CASCADE,
        related_name="folder_child",
        verbose_name="Parent Directory",
    )
    owner = models.ForeignKey(
        User,
        blank=False,
        help_text="Select the owner of the file",
        null=False,
        on_delete=models.CASCADE,
        related_name="folder_owner",
        verbose_name="Owner",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "parent", "owner"], name="unique_with_optional"
            ),
            models.UniqueConstraint(
                fields=["name", "owner"],
                condition=models.Q(parent=None),
                name="unique_without_optional",
            ),
        ]

class File(models.Model):
    file = models.FileField( 
                        blank=False,
                        help_text="Select a file to upload ",
                        null=False,
                        unique=False,
                        upload_to="files/",
                        verbose_name="File name", 
                        )
    parent = models.ForeignKey(
                Folder,
                blank=False,
                help_text="Select the parent directory",
                null=True,
                on_delete=models.CASCADE,
                related_name="file_child",
                verbose_name="Parent Directory",
                               )
    owner = models.ForeignKey(User, 
                              blank=False,
                              help_text="Select the owner of the file",
                              null=False,
                              on_delete=models.CASCADE,
                              related_name="file_owner",
                              verbose_name="Owner"
                              )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def name(self):
        return self.file.name.split("/")[-1]