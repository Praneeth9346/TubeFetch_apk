import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    # App Configuration
    page.title = "TubeFetch"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # --- LOGIC ---
    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "❌ Please enter a YouTube URL"
            status_text.color = "red"
            page.update()
            return

        # Disable button during download
        download_btn.disabled = True
        download_btn.text = "Downloading..."
        status_text.value = "⏳ Starting download..."
        status_text.color = "blue"
        page.update()

        try:
            # Android-specific configuration
            # We save to the internal storage "Download" folder
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
                'quiet': True,
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
            
            status_text.value = f"✅ Success!\nSaved to Downloads:\n{title}"
            status_text.color = "green"
            url_input.value = "" # Clear input

        except Exception as err:
            status_text.value = f"❌ Error: {str(err)}"
            status_text.color = "red"
        
        # Re-enable button
        download_btn.disabled = False
        download_btn.text = "Download MP4"
        page.update()

    # --- UI COMPONENTS ---
    logo_icon = ft.Icon(name=ft.icons.ONDEMAND_VIDEO, size=60, color="red")
    title_text = ft.Text("TubeFetch Mobile", size=24, weight="bold")
    
    url_input = ft.TextField(
        label="YouTube Link",
        hint_text="Paste https://youtube.com/...",
        width=300,
        text_align=ft.TextAlign.CENTER
    )
    
    download_btn = ft.ElevatedButton(
        text="Download MP4",
        icon=ft.icons.DOWNLOAD,
        on_click=download_click,
        bgcolor="red",
        color="white",
        width=200,
        height=50
    )
    
    status_text = ft.Text(size=14, text_align=ft.TextAlign.CENTER)

    # Add to page
    page.add(
        ft.Column(
            [
                logo_icon,
                title_text,
                ft.Divider(height=20, color="transparent"),
                url_input,
                ft.Divider(height=10, color="transparent"),
                download_btn,
                ft.Divider(height=20, color="transparent"),
                status_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
