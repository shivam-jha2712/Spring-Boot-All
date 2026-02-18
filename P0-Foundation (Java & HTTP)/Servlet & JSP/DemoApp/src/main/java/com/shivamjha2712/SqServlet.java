package com.shivamjha2712;

import java.io.IOException;
import java.io.PrintWriter;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

public class SqServlet extends HttpServlet {
	
	public void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {
		
//		int k = (int) req.getAttribute("k"); // Fetching data sent via RequestDispatcher (server-side forward).
//		int  k = Integer.parseInt(req.getParameter("k")); // Fetching data sent via URL Rewriting (query parameter).
		
//		HttpSession session = req.getSession(); // Retrieving the existing session.
//		int k =  (int)session.getAttribute("k"); // Fetching data from Session scope.
		
		int k = 0;
		// --- FETCHING COOKIES ---
		// There is no method to get a single cookie by name. You get the whole array.
		Cookie cookies[] = req.getCookies(); 
		
		// Iterate to find the specific cookie named "k".
		for(Cookie c : cookies) {
			if(c.getName().equals("k")) {
				k=Integer.parseInt(c.getValue()); // Parse String value back to int.
			}
		}
		
		
		
		k = k * k; // Perform the logic.
		
		PrintWriter out = res.getWriter(); 

		out.println("Squared result is " + k); // Send final output to browser.
		
		System.out.println("Sq is callled"); // Server-side log for debugging.
	}
}