import flet as ft
import os
import traceback

def main(page: ft.Page):
    page.title = "TubeFetch Debug"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.padding = 20

    # --- STATUS AREA ---
    status_text = ft.Text(value="Ready", size=16)
    
    def log(msg, color="white"):
        status_text.value = str(msg)
        status_text.color = color
        page.update()

    # --- DOWNLOAD LOGIC ---
    def download_click(e):
        url = url_input.value
        if not url:
            log("❌ Please enter a URL", "red")
            return

        download_btn.disabled = True
        log("⏳ Connecting to YouTube...", "blue")
        
        try:
            # 1. Define Download Path (Standard Android Download Folder)
            download_path = "/storage/emulated/0/Download"
            
            # 2. Check if we can write to this folder
            if not os.path.exists(download_path):
                log(f"❌ Error: Download folder not found at {download_path}", "red")
                download_btn.disabled = False
                return

            # 3. Configure yt-dlp (Removed 'ignoreerrors' to see real crashes)
            import yt_dlp
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'quiet': False, # Verbose logging
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # This line will now CRASH if there is an error (which is good!)
                # It allows us to catch the specific error below.
                info = ydl.extract_info(url, download=True)
                
                # Safety check
                if info is None:
                    log("❌ Download failed (Unknown reason)", "red")
                else:
                    title = info.get('title', 'Unknown Video')
                    log(f"✅ SUCCESS!\nSaved to: Download/{title}.mp4", "green")

        except Exception as err:
            # THIS IS THE IMPORTANT PART
            # It will print the REAL reason (e.g. "Permission Denied" or "No Internet")
            log(f"❌ FAILED:\n{str(err)}", "red")
        
        download_btn.disabled = False
        page.update()

    # --- UI LAYOUT ---
    url_input = ft.TextField(label="YouTube Link", hint_text="Paste link here")
    download_btn = ft.ElevatedButton("Download MP4", on_click=download_click, bgcolor="red", color="white")
    
    page.add(
        ft.Text("TubeFetch Mobile", size=24, weight="bold"),
        ft.Divider(),
        url_input,
        download_btn,
        ft.Divider(),
        ft.Text("Debug Log:", size=12, color="grey"),
        status_text
    )

ft.app(target=main)
