import React from 'react'
import axios from 'axios'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { useNavigate } from 'react-router-dom'

const Signin = () => {
    const [username, setUsername] = React.useState('')
    const [password, setPassword] = React.useState('')
    const navigate = useNavigate()


    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/login/', {
                username,
                password
            })
            if (response.status === 200 || response.status === 201) {
                // save in local storage
                window.localStorage.setItem('user', JSON.stringify(response))
                navigate('/user')
                toast.success('Login successful!')
            } else {
                toast.error('Login failed!')
            }

        } catch (error) {
            toast.error('Error Login. Please try again.')
        }

    }
    return (
        <>

            <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick pauseOnFocusLoss draggable pauseOnHover />
            <section className="py-5">
                <div className="container">
                    <div className="row justify-content-center">
                        <div className="col-md-6 col-lg-5">
                            <div className="card shadow rounded-4">
                                <div className="card-body p-4">
                                    <h2 className="text-center mb-4">Sign In</h2>
                                    <form onSubmit={handleSubmit}>
                                        <div className="mb-3">
                                            <label htmlFor="username" className="form-label">Username</label>
                                            <input
                                                type="text"
                                                id="username"
                                                className="form-control"
                                                value={username}
                                                onChange={(e) => setUsername(e.target.value)}
                                                required
                                            />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="password" className="form-label">Password</label>
                                            <input
                                                type="password"
                                                id="password"
                                                className="form-control"
                                                value={password}
                                                onChange={(e) => setPassword(e.target.value)}
                                                required
                                            />
                                        </div>
                                        <button type="submit" className="btn btn-primary w-100">Sign In</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </>
    )
}

export default Signin