package com.shivamjha2712;

import java.io.IOException;
import java.io.PrintWriter;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

public class AddServlet extends HttpServlet {

//	Req and Res are interfaces provided by the Servlet API (Tomcat). They represent the HTTP request and response.
//	public void service(HttpServletRequest req, HttpServletResponse res) throws IOException {
	// doGet is used here because the HTML form uses method="get".
	public void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException {
		// Parsing incoming parameters from the URL/Request body.
		int i = Integer.parseInt(req.getParameter("num1"));
		int j = Integer.parseInt(req.getParameter("num2"));
		int k = i + j;

		// System.out.println("result is " + k); // Prints to the server console (developer only).
		// PrintWriter sends data back to the client's browser (user visible).
//		PrintWriter out = res.getWriter(); 
//		
//		out.println("Added result is " + k);

		// --- 1. REQUEST DISPATCHER (Forwarding) ---
		// Happens internally on the server. Browser URL does NOT change.
		// Data is shared by attaching it to the request object.
		
//		req.setAttribute("k", k); // Key-Value pair attached to the request.
//		
//		RequestDispatcher rd = req.getRequestDispatcher("sq"); // Prepare to forward to 'sq'.
//		rd.forward(req, res); // Forward the request/response objects to the next servlet.
		
		
		// --- 2. URL REWRITING (Redirecting) ---
		// Tells the browser to make a NEW request to a different URL.
		// Data is passed by manually appending it to the URL string.
		// res.sendRedirect("sq?k="+k);
		
		// --- 3. SESSION MANAGEMENT (HttpSession) ---
		// Stores data on the server side, specific to a user session.
		// More secure and can hold objects, not just strings.
//		HttpSession session = req.getSession();
//		session.setAttribute("k", k); // Store 'k' in the session scope.
//		res.sendRedirect("sq");
		
		// --- 4. COOKIES (Client-Side State) ---
		// Stores a small piece of data on the user's browser.
		// Cookies only accept Strings. We convert int 'k' to String by appending "".
		Cookie cookie = new Cookie("k", k+""); 
		res.addCookie(cookie); // Send the cookie to the browser in the response header.
		res.sendRedirect("sq"); // Redirect client to the 'sq' servlet.
		
		
		
	}

}