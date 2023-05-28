
const copyBtn = [...document.getElementsByClassName('copy-btn')];




copyBtn.forEach(btn => btn.addEventListener('click', () => {
    //const secretText = btn.getAttribute('data-secret') 
    
    let copyTxt;
    copyTxt = document.getElementsByName("profile_link");
    console.log(copyTxt.textContent)
    copyTxt[0].textContent;
    
    navigator.clipboard.writeText(copyTxt[0].textContent)
    navigator.clipboard.readText().then(() => {
        btn.textContent = 'Copied'
        setTimeout((btn) => {btn.textContent = 'Copy to clipboard'}, 3000, btn)

    }).catch(() => {
        alert("Error copying secret to the clipboard")
    })
    
}))


