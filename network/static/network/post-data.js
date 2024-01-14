document.addEventListener("DOMContentLoaded" ,()=>{
  console.log("Post Script Linked")
  
  const tweet_button = document.querySelector("#tweet-btn")
  tweet_button.addEventListener("click" , ()=>{
    const data = document.querySelector("#tweet-form").value
    data_len = data.length
    if (data_len > 10){
      fetch('api/posts',{
        method : 'POST',
        body : JSON.stringify({
          "user_post" : data
        })
      })
      .then(Response => console.log(Response.status))
      document.querySelector("#tweet-form").value = " "
    }
    else{
      alert("Minimum Tweet char should be 10.")
    }
  })
})