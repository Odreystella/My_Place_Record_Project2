function buildQuery(params) {
    return Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&')
}

function buildUri(baseUrl, queries) {
    return baseUrl + '?' + buildQuery(queries)
}

// 네이버 로그인
function naverLogin(){
    params = {
        response_type: 'code',                // response_type는 항상 code, 네아로한 사용자의 회원정보를 이용해서 서버에 회원가입 시키고 회원정보 저장할 예정
        client_id: 'BmJKMhPBKR4VdcrQTqYG',
        redirect_uri: location.origin + '/user/login/social/naver/callback/' + location.search, // 네이버에 앱 등록할 떄 입력한 Callback URL, 쿼리 파라미터가 있을 경우 거기로 redirect
        state: document.querySelector('[name=csrfmiddlewaretoken]').value   // csrf등의 공격으로 사용자가 해당 서비스를 접속하지 않고 소셜로그인을 시도하는 경우를 차단하기 위해 필요한 값
    }
    url = buildUri('https://nid.naver.com/oauth2.0/authorize', params)
   
    location.replace(url)  //  url로 화면 전환, 전환된 화면은 네이버에서 제공하는 화면으로 컨트롤할 수 없음
}


