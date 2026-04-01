function toggleAudio(id, box) {

    const audios = document.querySelectorAll("audio");

    audios.forEach(a => {
        if (a.id !== "audio-" + id) {
            a.pause();
            resetRow(a.id.replace("audio-", ""));
        }
    });

    const audio = document.getElementById("audio-" + id);
    const icon = document.getElementById("icon-" + id);
    const progress = document.getElementById("progress-" + id);

    if (audio.paused) {
        audio.play();
        icon.className = "bi bi-pause-fill";
    } else {
        audio.pause();
        icon.className = "bi bi-play-fill";
    }

    audio.ontimeupdate = () => {
        if (audio.duration) {
            const percent = (audio.currentTime / audio.duration) * 100;
            progress.style.width = percent + "%";
        }
    };

    audio.onended = () => {
        resetRow(id);
    };
}

function resetRow(id) {
    const audio = document.getElementById("audio-" + id);
    const icon = document.getElementById("icon-" + id);
    const progress = document.getElementById("progress-" + id);

    if (audio) audio.pause();
    if (icon) icon.className = "bi bi-play-fill";
    if (progress) progress.style.width = "0%";
}