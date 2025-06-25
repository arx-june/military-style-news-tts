(function() {
    // Block any accidental <button type="submit">
    document.addEventListener("click", (e) => {
      if (e.target.tagName === "BUTTON" && e.target.type === "submit") {
        e.preventDefault();
        console.log("Blocked a submit-button click");
      }
    });
  
    // Grab all elements
    const uploadContainer         = document.getElementById("upload-container");
    const processingContainer     = document.getElementById("processing-container");
    const voiceSelectionContainer = document.getElementById("voice-selection-container");
    const audioPlayerContainer    = document.getElementById("audio-player-container");
    const uploadArea              = document.getElementById("upload-area");
    const fileInput               = document.getElementById("file-input");
    const processingStatus        = document.getElementById("processing-status");
    const imagePreview            = document.getElementById("image-preview");
    const errorContainer          = document.getElementById("error-container");
    const generateAudioBtn        = document.getElementById("generate-audio-btn");
    const audioPlayer             = document.getElementById("audio-player");
    const playBtn                 = document.getElementById("play-btn");
    const pauseBtn                = document.getElementById("pause-btn");
    const replayBtn               = document.getElementById("replay-btn");
    const homeBtn                 = document.getElementById("home-btn");
    const frequencyVisualizer     = document.getElementById("frequency-visualizer");
    const extractedTextContainer  = document.getElementById("extracted-text");
    const bgMusicForm             = document.getElementById("bg-music-form");
    const bgMusicFileInput        = document.getElementById("bg-music-file");
    const bgMusicListContainer    = document.getElementById("bg-music-list");
    const listBgMusicBtn          = document.getElementById("list-bg-music-btn");
  
    let processedImageId = null;
  
    // 1) Image Upload Handler
    uploadArea.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", handleImageUpload);
    uploadArea.addEventListener("dragover", handleDragOver);
    uploadArea.addEventListener("drop", handleDrop);
  
    // 2) Generate Audio Handler
    generateAudioBtn.addEventListener("click", (evt) => {
      evt.preventDefault();
      console.log("⚡️ [Generate click] processedImageId:", processedImageId);
      handleVoiceSelection();
    });
  
    // 3) Audio Controls
    playBtn.addEventListener("click", () => audioPlayer.play());
    pauseBtn.addEventListener("click", () => audioPlayer.pause());
    replayBtn.addEventListener("click", () => {
      audioPlayer.currentTime = 0;
      audioPlayer.play();
    });
    homeBtn.addEventListener("click", resetApp);
  
    // 4) Background Music
    bgMusicForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      console.log("Uploading background music...");
      const file = bgMusicFileInput.files[0];
      if (!file) return alert("Please select a music file");
      const formData = new FormData();
      formData.append("music", file);
      try {
        const res = await fetch("/api/upload-background-music", { method: "POST", body: formData });
        const data = await res.json();
        console.log("Upload BGM response:", data);
        alert(data.success ? "Background music uploaded successfully" : `Upload failed: ${data.message}`);
        if (data.success) bgMusicFileInput.value = "";
      } catch (err) {
        console.error("Upload BGM error:", err);
        alert("Error uploading music");
      }
    });
  
    listBgMusicBtn.addEventListener("click", async () => {
      console.log("Listing background music...");
      try {
        const res = await fetch("/api/list-background-music");
        const data = await res.json();
        console.log("List BGM response:", data);
        bgMusicListContainer.innerHTML = data.success
          ? `<ul>${data.music_files.map(f => `<li>${f}</li>`).join("")}</ul>`
          : "<p>No background music files available.</p>";
      } catch (err) {
        console.error("List BGM error:", err);
        bgMusicListContainer.innerHTML = "<p>Error fetching background music files.</p>";
      }
    });
  
    // Handlers & Helpers
  
    function handleDragOver(e) {
      e.preventDefault(); e.stopPropagation();
      uploadArea.classList.add("drag-over");
    }
  
    function handleDrop(e) {
      e.preventDefault(); e.stopPropagation();
      uploadArea.classList.remove("drag-over");
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleImageUpload();
      }
    }
  
    async function handleImageUpload() {
      console.log("Starting image upload...");
      const file = fileInput.files[0];
      if (!file) return showError("Please select an image file");
      if (!file.type.match("image.*")) return showError("Please select a valid image file");

      if (file.size > 16 * 1024 * 1024) { // 16MB limit
        return showError("File size too large. Maximum 16MB allowed.");
      }
  
      showSection(processingContainer);
      frequencyVisualizer.style.display = "flex";
  
      const formData = new FormData();
      formData.append("image", file);
  
      try {
        const reader = new FileReader();
        reader.onload = e => {
          imagePreview.src = e.target.result;
          imagePreview.style.display = "block";
        };
        reader.readAsDataURL(file);
  
        const res = await fetch("/api/process-image", { method: "POST", body: formData });
        const data = await res.json();
        console.log("Process-image response:", data);
        if (!data.success) throw new Error(data.message);
  
        processedImageId = data.imageId;
        console.log("Image processed, id =", processedImageId);
        setTimeout(() => {
          frequencyVisualizer.style.display = "none";
          showSection(voiceSelectionContainer);
        }, 1000);
      } catch (err) {
        console.error("handleImageUpload error:", err);
        showError(err.message);
        showSection(uploadContainer);
      }
    }
  
    async function handleVoiceSelection() {
      console.log("handleVoiceSelection() start");
      const voice = document.getElementById("voice-select").value;
      const addBG = document.getElementById("bg-music-checkbox").checked;
      console.log("Voice:", voice, "AddBG:", addBG);
  
      if (!processedImageId) {
        console.warn("No processedImageId, aborting");
        return showError("No processed image found");
      }
  
      processingStatus.textContent = "Generating audio briefing...";
      showSection(processingContainer);
      frequencyVisualizer.style.display = "flex";
  
      try {
        console.log("Calling /api/generate-audio...");
        const res = await fetch("/api/generate-audio", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ imageId: processedImageId, voice, addBackgroundMusic: addBG }),
        });
        const data = await res.json();
        console.log("generate-audio response:", data);
        if (!data.success) throw new Error(data.message);
  
        audioPlayer.src = data.audioUrl;
        console.log("Audio URL set:", data.audioUrl);
        extractedTextContainer.innerText = data.extractedText;
        console.log("Extracted text set.");
  
        setTimeout(() => {
          frequencyVisualizer.style.display = "none";
          console.log("Switching to audioPlayerContainer");
          showSection(audioPlayerContainer);
        }, 1000);
      } catch (err) {
        console.error("handleVoiceSelection error:", err);
        showError(err.message);
        showSection(voiceSelectionContainer);
      }
    }
  
    function showSection(sec) {
      document.querySelectorAll("section").forEach(s => (s.style.display = "none"));
      sec.style.display = "flex";
      console.log("showSection:", sec.id);
    }
  
    function showError(msg) {
      console.log("showError:", msg);
      errorContainer.innerHTML = `<div class="error-message">${msg}</div>`;
      setTimeout(() => (errorContainer.innerHTML = ""), 5000);
    }
  
    function resetApp() {
      console.log("resetApp()");
      showSection(uploadContainer);
      fileInput.value = "";
      imagePreview.style.display = "none";
      processedImageId = null;
      audioPlayer.pause();
      audioPlayer.src = "";
      frequencyVisualizer.style.display = "none";
    }
  })();
  