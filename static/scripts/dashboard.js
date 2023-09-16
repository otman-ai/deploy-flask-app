let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");
let mainContent = document.getElementById('content');


toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

// Use JavaScript to make an AJAX request to the Flask endpoint



const videoElement = document.getElementById('camera-feed');
const modal = document.getElementById('myModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementsByClassName('close')[0];
const submitStreamBtn = document.getElementById('submitStreamBtn');
const error_config = document.querySelector(".error-confi")
document.getElementById('addStreamBtn').addEventListener('click', function () {
  document.getElementById('ipAddress').value = '';
  document.getElementById('port').value = '';
  modal.style.display = 'block';
  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });
  error_config.style.display = 'none';


});

submitStreamBtn.addEventListener('click',async function(){
  error_config.style.display = 'none';
  let ipAddress = document.getElementById('ipAddress').value;
  let port = document.getElementById('port').value;
  if (ipAddress && port) {
    const data = {
      ipAddress: ipAddress,
      port: port
    };
    const config_ = `http://${ipAddress}:${port}/video`
    await fetch(config_, { method: 'HEAD' })
      .then(function (response) {
        if (response.status === 200) {
          console.log("Website is up and running.");
          const re = fetch('/dash', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) 
          })
          setTimeout(function() {
            location.reload();
        }, 1000); 
          ipAddress.value = "";
          port.value = "";
          modal.style.display = 'none';
        } else {
          console.log("Website returned status code " + response.status + ".");
        }
      })
      .catch(function (error) {
        error_config.style.display = 'block';
        console.log("Error: " + error.message + ". Website might be down or unreachable.");
      });
      
  }
 
}  
);
document.addEventListener("DOMContentLoaded", function () {

    const removeButtons = document.querySelectorAll(".remove-button");
    removeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const cameraId = this.getAttribute("alt");
            console.log(cameraId)
            if (confirm("Are you sure you want to remove this camera?")) {
                fetch(`/remove_camera/${cameraId}`, {
                    method: "DELETE",
                })
                .then(response => {
                    if (response.ok) {
                        // Reload the page or update the UI as needed
                        window.location.reload();
                    } else {
                        alert("Error removing camera.");
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("An error occurred while removing the camera.");
                });
            }
        });
    });
    CheckAnyUpdate();
   

});
async function checkIpAddress(ip) {
  try {
    const response = await fetch(ip, { method: 'HEAD' });
    if (response.status === 200) {
      return true; 
    }
    return false; 
  } catch {
    return false; 
  }
}
function CheckAnyUpdate(){
  console.log("h");
  const camera_img = document.querySelectorAll(".camera_img");
  const camera_img_detect = document.querySelectorAll(".camera_img-detect");

  fetch('/check_ips')
      .then(response => response.json())
      .then(async data => {
        const _ip_adresses_to_check = data.ip_adresses;
        const ids = data.ids;
        camera_img.forEach(img => {
          for(let i = 0; i<_ip_adresses_to_check.length;i++){
            let para = document.getElementById(ids[i]);
            let para_detection = document.getElementById(`${ids[i]}-detection`);

            checkIpAddress(_ip_adresses_to_check[i])
            .then(isWorking => {
              camera_img_detect.forEach(img_ => {
                if(!isWorking){img_.src = "static/imgs/offline/h.jpg"; }
                else{ img_.src = `/video_annotated/${ids[i]}`}
              });
              if (isWorking){
                img.src = _ip_adresses_to_check[i];
                img.style.border = '3px solid #000';
               para.innerHTML = "Online";
               para.style.backgroundColor = "rgb(92, 240, 100)";
               para_detection.innerHTML = "Detecting..";
              }
              else {
                img.style.border = 'none';
                para.innerHTML = "Offline";
                para.style.backgroundColor = "rgb(255, 98, 98)";
                para_detection.innerHTML = "Nothing to detect";
                img.src = "static/imgs/offline/h.jpg";               
              }
            });
          }
        });

      })

}
// fix bugs 
// add more security to the platform

CheckAnyUpdate()
const intervalId = setInterval(CheckAnyUpdate, 10000);