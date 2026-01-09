import flet as ft
import os
import traceback

def main(page: ft.Page):
    page.title = "TubeFetch Safe Mode"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.padding = 20

    # --- 1. DIAGNOSTIC LOAD ---
    # We try to import yt_dlp inside the app to catch crash errors
    lib_status = ft.Text("Initializing...", color="yellow")
    page.add(lib_status)
    
    yt_dlp = None
    try:
        import yt_dlp as lib
        yt_dlp = lib
        lib_status.value = "✅ Library Loaded Successfully!"
        lib_status.color = "green"
    except Exception as e:
        error_msg = traceback.format_exc()
        lib_status.value = f"❌ CRITICAL ERROR:\n{error_msg}"
        lib_status.color = "red"
        page.update()
        return  # Stop here if library is broken

    page.update()

    # --- 2. MAIN APP LOGIC (Only runs if library loaded) ---
    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "Please enter a URL"
            page.update()
            return

        download_btn.disabled = True
        status_text.value = "⏳ Starting..."
        page.update()

        try:
            # Android Download Path
            download_path = "/storage/emulated/0/Download"
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'quiet': True,
                'nocheckcertificate': True,
                'ignoreerrors': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
            
            status_text.value = f"✅ Saved to: Download/{title}.mp4"
            status_text.color = "green"

        except Exception as err:
            # Show full error on screen
            status_text.value = f"❌ Error: {str(err)}"
            status_text.color = "red"
        
        download_btn.disabled = False
        page.update()

    # --- UI COMPONENTS ---
    url_input = ft.TextField(label="YouTube Link")
    download_btn = ft.ElevatedButton("Download", on_click=download_click)
    status_text = ft.Text()

    page.add(
        ft.Divider(),
        url_input,
        download_btn,
        status_text
    )

ft.app(target=main)
