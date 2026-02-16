package com.shivamjha2712;

import java.io.IOException;
import java.io.PrintWriter;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class AddServlet extends HttpServlet
{
	
	public void service(HttpServletRequest req, HttpServletResponse res) throws IOException {
		int i  = Integer.parseInt(req.getParameter("num1"));
		int j = Integer.parseInt(req.getParameter("num2"));
		int k = i + j;
		
		// System.out.println("result is " + k); // This will be printing the data on a console and while working with java EE we don't want it we want it to be printed on ui.
		PrintWriter out = res.getWriter(); 
		
		out.println("result is " + k);
	}
	
}
