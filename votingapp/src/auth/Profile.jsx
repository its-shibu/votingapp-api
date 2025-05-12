import React from 'react'

const Profile = () => {
    const user = JSON.parse(window.localStorage.getItem('user'))
    // const username = user.data.username
    return (
        <>
            <h2>
                Valid Token : {user.data.token}
            </h2>
            <h2>
                UserName : {user.data.username}
            </h2>
            <h2>
                Password : {user.data.password}
            </h2>
        </>
    )
}

export default Profile