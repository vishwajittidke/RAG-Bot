const f=document.getElementById("f"),q=document.getElementById("q"),chat=document.getElementById("chat"),btn=document.getElementById("send");
const uploadBtn=document.getElementById("uploadBtn"), fileInput=document.getElementById("fileInput"), uploadStatus=document.getElementById("uploadStatus");

let history = JSON.parse(localStorage.getItem("chatHistory")) || [];
function saveHistory() { localStorage.setItem("chatHistory", JSON.stringify(history)); }
function renderHistory() {
    chat.innerHTML = "";
    if (history.length === 0) {
        history.push({ text: "Hello! Ask me anything.", sender: "bot" });
        saveHistory();
    }
    history.forEach(m => {
        let d=document.createElement("div");
        d.className="msg "+m.sender;
        if(m.sender === "bot") d.innerHTML = typeof marked !== "undefined" ? marked.parse(m.text) : m.text;
        else d.textContent = m.text;
        chat.appendChild(d);
    });
    chat.scrollTop = chat.scrollHeight;
}

function add(t,c,save=true){
    let d=document.createElement("div");
    d.className="msg "+c;
    if(c === "bot") d.innerHTML = typeof marked !== "undefined" ? marked.parse(t) : t;
    else d.textContent = t;
    chat.appendChild(d);
    chat.scrollTop=chat.scrollHeight;
    if(save){
        history.push({ text: t, sender: c });
        saveHistory();
    }
}
renderHistory();

function typing(){let d=document.createElement("div");d.className="typing";d.id="typing";d.innerHTML='<div class="dot"></div><div class="dot"></div><div class="dot"></div>';chat.appendChild(d);chat.scrollTop=chat.scrollHeight;}
function stopTyping(){let t=document.getElementById("typing");if(t)t.remove();}

q.addEventListener("input",()=>{q.style.height="auto";q.style.height=q.scrollHeight+"px";});

q.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        btn.click();
    }
});

uploadBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) return alert("Please select a file.");
    
    const formData = new FormData();
    formData.append("file", file);
    
    uploadBtn.disabled = true;
    uploadStatus.textContent = "Uploading...";
    uploadStatus.style.color = "#666";
    
    try {
        const res = await fetch("/upload", { method: "POST", body: formData });
        const data = await res.json();
        if(res.ok) {
            uploadStatus.textContent = "Document indexed!";
            uploadStatus.style.color = "green";
        } else {
            uploadStatus.textContent = data.detail || "Upload failed.";
            uploadStatus.style.color = "red";
        }
    } catch(e) {
        uploadStatus.textContent = "Error during upload.";
        uploadStatus.style.color = "red";
    }
    uploadBtn.disabled = false;
});

f.onsubmit=async(e)=>{e.preventDefault();let text=q.value.trim();if(!text)return;add(text,"user");q.value="";q.style.height="auto";btn.disabled=true;q.disabled=true;typing();
try{
let r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:text})});
let data=await r.json();stopTyping();add(data.text,"bot");
}catch(e){stopTyping();add("Unable to reach AI backend.","bot");}
btn.disabled=false;q.disabled=false;q.focus();};