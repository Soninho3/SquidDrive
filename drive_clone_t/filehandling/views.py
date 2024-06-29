from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views import View
from filehandling.models import File
from filehandling.models import Folder
from drive_clone_t.utils import add_error, get_errors


class HomeView(LoginRequiredMixin, View):
    """
    Displays the home page.
    """

    def get(self, request):
        errors = get_errors(request=request, url_name="home")
        folders = Folder.objects.filter(owner=request.user, parent=None)
        files = File.objects.filter(owner=request.user, parent=None)

        return render(
            request, "filehandling/home.html", {"errors": errors, "files": files, "folders": folders}
        )


class CreateFolderView(LoginRequiredMixin, View):
    """
    Create folder endpoint view.
    """

    def post(self, request, parent_id=None):
        data = request.POST
        name = data.get("name")

        if not name:
            add_error(
                request=request,
                tag="folder_error",
                message="The folder name cannot be empty.",
                url_name="home" if not parent_id else "folder_detail",
            )
            return redirect("home") if not parent_id else redirect("folder_detail")

        if parent_id:
            try:
                parent = Folder.objects.get(id=parent_id)

            except Folder.DoesNotExist:
                add_error(
                    request=request,
                    tag="global_error",
                    message="The folder does not exist.",
                    url_name="home",
                )
                return redirect("home")

            if parent.owner != request.user:
                add_error(
                    request=request,
                    tag="global_error",
                    message="You do not have permission to access this folder.",
                    url_name="home",
                )
                return redirect("home")

            folder = Folder(name=name, parent=parent, owner=request.user)

        else:
            folder = Folder(name=name, owner=request.user)

        try:
            folder.save()

        except IntegrityError:
            add_error(
                request=request,
                tag="folder_error",
                message="A folder with the same name already exists in the selected directory.",
                url_name="home",
            )

        return (
            redirect("home")
            if not parent_id
            else redirect("folder_detail", folder_id=parent_id)
        )


class UploadFileView(LoginRequiredMixin, View):
    """
    Upload file endpoint view.
    """

    def post(self, request, parent_id=None):
        file = request.FILES.get("file")

        if not file:
            add_error(
                request=request,
                tag="file_error",
                message="No file selected.",
                url_name="home" if not parent_id else "folder_detail",
            )
            return (
                redirect("home")
                if not parent_id
                else redirect("folder_detail", folder_id=parent_id)
            )

        if parent_id:
            try:
                folder = Folder.objects.get(id=parent_id)

            except Folder.DoesNotExist:
                add_error(
                    request=request,
                    tag="global_error",
                    message="The folder does not exist.",
                    url_name="home",
                )
                return redirect("home")

            if folder.owner != request.user:
                add_error(
                    request=request,
                    tag="global_error",
                    message="You do not have permission to access this folder.",
                    url_name="home",
                )
                return redirect("home")

            new_file = File(parent=folder, owner=request.user, file=file)

            new_file.save()
            return redirect("folder_detail", folder_id=parent_id)

        new_file = File(parent=None, owner=request.user, file=file)

        new_file.save()
        return redirect("home")


class FolderView(LoginRequiredMixin, View):
    """
    Displays the folder page.
    """

    def get(self, request, folder_id: int):
        errors = get_errors(request=request, url_name="folder_detail")

        try:
            folder = Folder.objects.get(id=folder_id)

        except Folder.DoesNotExist:
            add_error(
                request=request,
                tag="global_error",
                message="The folder does not exist.",
                url_name="home",
            )
            return redirect("home")

        if folder.owner != request.user:
            add_error(
                request=request,
                tag="global_error",
                message="You do not have permission to access this folder.",
                url_name="home",
            )
            return redirect("home")

        folders = Folder.objects.filter(owner=request.user, parent=folder)
        files = File.objects.filter(owner=request.user, parent=folder)

        return render(
            request,
            "filehandling/home.html",
            {
                "errors": errors,
                "files": files,
                "folders": folders,
                "folder": folder,
                "parent_folder": folder.parent,
            },
        )
