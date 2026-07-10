$ErrorActionPreference = "Stop"

$audioDir = Join-Path $PSScriptRoot "..\public\audio"
$voiceDir = Join-Path $audioDir "voice"
New-Item -ItemType Directory -Force $voiceDir | Out-Null

$scenes = @(
    @{ Id = "hook"; Text = "I'm Codex. Sachin had an idea: what if repetitive office work could happen in seconds?" },
    @{ Id = "plan"; Text = "He brought the problem. I helped turn it into a plan, and then into a working product." },
    @{ Id = "architecture"; Text = "Together, we built OfficeFlow: a modern React interface backed by FastAPI, with four practical workflows behind a clean API." },
    @{ Id = "minutes"; Text = "Meeting audio becomes a transcript, structured minutes, action items, and a downloadable Word document." },
    @{ Id = "inbox"; Text = "Messy emails are sorted by priority, summarized, and paired with professional draft replies." },
    @{ Id = "documents"; Text = "A single C S V becomes personalized documents, generated in one batch and packaged together." },
    @{ Id = "ask"; Text = "A policy P D F becomes a conversation, returning precise answers with page citations." },
    @{ Id = "backend"; Text = "Built with Codex and powered at runtime by Gemini, OfficeFlow also has guarded operations and provider fallbacks to keep it dependable." },
    @{ Id = "demo"; Text = "When the internet disappears, Demo Mode keeps the presentation moving." },
    @{ Id = "close"; Rate = "+15%"; Text = "One student. One AI collaborator. One working idea. Built by Sachin, with the help of ChatGPT's Codex." }
)

foreach ($scene in $scenes) {
    $out = Join-Path $voiceDir ($scene.Id + ".mp3")
    $rate = if ($scene.Rate) { $scene.Rate } else { "+2%" }
    & edge-tts --voice "en-US-AndrewMultilingualNeural" --rate=$rate --text $scene.Text --write-media $out
    if ($LASTEXITCODE -ne 0) { throw "Voice generation failed for $($scene.Id)." }
}

$downloads = @{
    "music-stylz.mp3" = "https://assets.mixkit.co/music/102/102.mp3"
    "whoosh.wav" = "https://remotion.media/whoosh.wav"
    "switch.wav" = "https://remotion.media/switch.wav"
    "ding.wav" = "https://remotion.media/ding.wav"
}

foreach ($item in $downloads.GetEnumerator()) {
    Invoke-WebRequest -UseBasicParsing $item.Value -OutFile (Join-Path $audioDir $item.Key)
}

Write-Output "Generated $($scenes.Count) voice clips and downloaded licensed audio assets."
