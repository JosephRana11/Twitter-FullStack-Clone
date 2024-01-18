document.addEventListener("DOMContentLoaded" ,()=>{
  
  const post_audio = new Audio('static/network/post.mp3')

  console.log("Post Script Linked")
  function toggle_loader(){
    console.log("Toggle Loader Initalized")
    const loader = document.querySelector("#loader_div")
    if (loader.style.display == "flex"){
      loader.style.display = "none"
    }
    else {
      loader.style.display = "flex"
      
    }
  }

  
  const tweet_button = document.querySelector("#tweet-btn")
  tweet_button.addEventListener("click" , ()=>{
    const data = document.querySelector("#tweet-form").value
    data_len = data.length
    console.log(data_len)
    if (data_len > 10){
      toggle_loader()
      loader_interval = setInterval(turn_of_loader , 1000)
      fetch('api/posts',{
        method : 'POST',
        body : JSON.stringify({
          "user_post" : data
        })
      })
      .then(Response => console.log(Response.status))
    }
    else{
      alert("Minimum Tweet char should be 10.")
    }
  })
  function turn_of_loader(){
    clearInterval(loader_interval)
    toggle_loader()
    document.querySelector("#tweet-form").value = ""
    location.reload()
    document.querySelector("#tweet-form").setAttribute("placeholder" , "What's on your Mind?")
  }
})