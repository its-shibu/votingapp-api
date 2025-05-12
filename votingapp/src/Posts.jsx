import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Posts = () => {
    const [posts, setPosts] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const res = await axios.get('http://127.0.0.1:8000/api/posts/');
                setPosts(res.data);
            } catch (err) {
                console.error(err);
                setError('Failed to load posts');
            }
        };

        fetchPosts();
    }, []);

    return (
        <>
            <h2>Posts</h2>
            <div className="container d-flex flex-wrap overflow-hidden">
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div className="row">
                    {posts.map((post, i) => (
                        <div className="col-md-3 shadow p-3 m-2" key={i}>
                            <h4>{post.title}</h4>
                            <a href={post.url}>{post.url}</a>
                            <p>Votes: {post.votes}</p>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
};

export default Posts;
