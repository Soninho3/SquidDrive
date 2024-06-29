from django.urls import path
from filehandling.views import CreateFolderView, FolderView, HomeView, UploadFileView

urlpatterns = [
    # Home
    path("", HomeView.as_view(), name="home"),
    # File
    path("file/upload", UploadFileView.as_view(), name="upload_file"),
    path("file/upload/<int:parent_id>", UploadFileView.as_view(), name="upload_file"),
    # Folder
    path("folder/<int:folder_id>", FolderView.as_view(), name="folder_detail"),
    path("folder/create", CreateFolderView.as_view(), name="folder_create"),
    path(
        "folder/create/<int:parent_id>",
        CreateFolderView.as_view(),
        name="folder_create",
    ),
]
