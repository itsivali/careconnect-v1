import React from "react";


function LogIn(){
    return(
        <div className="login">
            <h1>Please Login to Your Account.</h1>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Username</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Enter your full name"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Password</label>
                <input type="password" class="form-control" id="exampleFormControlInput1" placeholder="Enter your password"></input>
            </div>
        </div>
    )
}
export default LogIn;