document.addEventListener("DOMContentLoaded" , ()=>{
  console.log("Notifications Section Console")

  fetch('/api/user/notifications')
  .then(Response => Response.json())
  .then(posts => {
    posts.forEach( post => {
      console.log(post)
      const main_div = document.createElement("div")
      main_div.className = "card"
      main_div.style.width = "80%"
  
      const body = document.createElement("div")
      body.className = "card-body"
      body.innerHTML = post.notification_text

      const footer = document.createElement("div")
      footer.className = "blockquote-footer"
      footer.innerHTML = post.notification_date

      
      const footer_div = document.createElement("div")
      footer_div.className = "notification_footer_div"
      footer_div.appendChild(footer)

      main_div.append(body)
      main_div.append(footer_div)
      document.querySelector("#notifications_div").appendChild(main_div)
    })
  })
})