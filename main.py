import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    page.title = "TubeFetch Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "adaptive"

    # --- LOGIC ---
    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "❌ Please enter a URL"
            status_text.color = "red"
            page.update()
            return

        status_text.value = "⏳ Fetching info..."
        status_text.color = "blue"
        progress_ring.visible = True
        download_btn.disabled = True
        page.update()

        try:
            # OPTIMIZED FOR ANDROID:
            # We use 'best' (single file) instead of 'bestvideo+bestaudio'.
            # Why? Because merging requires FFmpeg, which is very hard to get working on Android.
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s', # Android Download Folder
                'quiet': True,
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
                
            status_text.value = f"✅ Saved to Downloads:\n{title}"
            status_text.color = "green"
            
        except Exception as err:
            status_text.value = f"❌ Error: {str(err)}"
            status_text.color = "red"
        
        progress_ring.visible = False
        download_btn.disabled = False
        page.update()

    # --- UI LAYOUT ---
    title = ft.Text("TubeFetch Mobile", size=30, weight="bold", color="red")
    url_input = ft.TextField(label="YouTube URL", hint_text="Paste link here...")
    
    download_btn = ft.ElevatedButton(
        text="Download MP4",
        icon=ft.icons.DOWNLOAD,
        on_click=download_click,
        bgcolor="red",
        color="white"
    )
    
    progress_ring = ft.ProgressRing(visible=False)
    status_text = ft.Text(size=16)

    # Add components to page
    page.add(
        ft.Column(
            [
                title,
                ft.Divider(),
                url_input,
                download_btn,
                progress_ring,
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main)
