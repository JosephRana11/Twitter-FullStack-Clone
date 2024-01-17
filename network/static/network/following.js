document.addEventListener("DOMContentLoaded" , ()=>{
  console.log("Welcome to Following Page Console")
  fetch("/api/following")
  .then(Response => Response.json())
  .then(posts => {
    const like_audio = new Audio("static/network/like.mp3")
    posts.forEach(post => {
      const main_div = document.createElement("div")
      main_div.className = "card"
      main_div.style.width = "80%"
  
      const header = document.createElement("div")
      header.className = "card-header"
      header.style.fontWeight = "300"

      const username_header = document.createElement("a")
      username_header.setAttribute("href" , `/user/${post.owner}`)
      username_header.innerHTML = `@${post.owner}`

      header.appendChild(username_header)
      
      const body = document.createElement("div")
      body.className = "card-body"
      body.innerHTML = post.text

      const footer = document.createElement("div")
      footer.className = "blockquote-footer"
      footer.innerHTML = post.posted_at

      const like = document.createElement("i")
      like.className = "fa-regular fa-heart fa-2x"
      like.id = `post${post.id}`
      like.setAttribute("data-state" , 0)
      like.style.color = "#F08080"
      like.addEventListener("click" , ()=>{toggle_like(post.id)})

      const like_count = document.createElement("div")
      like_count.innerHTML = post.likes
      like_count.id = `likeCount${post.id}`
      like_count.className = "like-count"

      const like_div = document.createElement("div")
      like_div.className = "like-div"
      like_div.appendChild(like)
      like_div.appendChild(like_count)

      const footer_div = document.createElement("div")
      footer_div.className = "footer_div"
      footer_div.appendChild(like_div)
      footer_div.appendChild(footer)
  
  
      main_div.appendChild(header)
      main_div.appendChild(body)
      main_div.appendChild(footer_div)
  
      document.querySelector("#posts-container").append(main_div)
    })
    fetch('api/likes')
    .then(response => {
      if (response.status == 204){
        return []
      }
      else{
        return response.json()
      }
    }
    )
    .then(likes =>{
      likes.forEach(like => {
        const current_like = document.querySelector(`#post${like.post}`)
        if (current_like != null){
         current_like.className = "fa-solid fa-heart fa-2x"
         current_like.style.color = "#F08080"
         current_like.dataset.state = 1
         console.log(current_like.dataset.state)}
      })
    })
  
    function toggle_like(id){
      const current_like = document.querySelector(`#post${id}`)
      const like_count = document.querySelector(`#likeCount${id}`).innerHTML
      if (current_like.dataset.state == 0){
        like_audio.play()
        current_like.className = "fa-solid fa-heart fa-2x"
        current_like.dataset.state = 1
        console.log(id)
        fetch('api/likes', {
          method : 'POST',
          body :  JSON.stringify({post_id:id}),
        })
        .then(response => console.log(response.status))
        document.querySelector(`#likeCount${id}`).innerHTML = parseInt(like_count) + 1
      }
      else{
        current_like.className = "fa-regular fa-heart fa-2x"
        current_like.style.color = "#F08080"
        current_like.dataset.state = 0
        fetch('api/likes' , {
          method : 'DELETE',
          body : JSON.stringify({post_id:id})
        })
        .then(response => (console.log(response.status)))
        document.querySelector(`#likeCount${id}`).innerHTML = parseInt(like_count) - 1
      }
    }  
    });
  
})