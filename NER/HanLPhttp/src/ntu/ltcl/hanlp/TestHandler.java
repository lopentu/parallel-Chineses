package ntu.ltcl.hanlp;

import java.io.IOException;
import com.sun.net.httpserver.HttpExchange;

public class TestHandler extends Handler {
  public void handle(HttpExchange httpExchange) throws IOException {
    System.out.println("GET:/test");

    writeResponse(httpExchange, "It works.");
  }
}
