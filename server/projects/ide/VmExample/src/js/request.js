import axios from "axios";

function get(baseURL, success_callback, url) {
  axios.get('/corstests/get_csrf_token_with_cookie/', {
    baseURL: baseURL ? baseURL : 'http://localhost:8000',
    withCredentials: true
  }).then(res => {
    if (res.status == 200) {
      let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
      this.csrftoken = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
      if (success_callback) {
        success_callback(url, baseURL)
      }
    }
    else {
    }
  })
  .catch(function (error) {
    ElMessage({
      message: `get token failure, error=${error}`,
      type: 'failure',
    });
  });
}