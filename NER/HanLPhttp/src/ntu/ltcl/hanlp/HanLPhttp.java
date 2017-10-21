package ntu.ltcl.hanlp;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.List;
import java.util.stream.Collectors;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.hankcs.hanlp.corpus.tag.Nature;

public class HanLPhttp {

  public static void main(String[] args) throws Exception {
    HttpServer server = HttpServer.create(new InetSocketAddress(5217), 0);

    server.createContext("/test", new TestHandler());
    server.createContext("/test/", new TestHandler());

    server.createContext("/name", new NameHandler());
    server.createContext("/name/", new NameHandler());

    server.setExecutor(null);

    server.start();
  }

  // Test handler
  static class TestHandler implements HttpHandler {
    public void handle(HttpExchange httpExchange) throws IOException {
      System.out.print("GET:/test ... ");
      System.out.println(httpExchange.getRequestURI().getQuery());

      byte[] response = "It works.".getBytes();
      httpExchange.sendResponseHeaders(200, response.length);

      OutputStream os = httpExchange.getResponseBody();
      os.write(response);
      os.close();
    }
  };

  // Name handler
  static class NameHandler implements HttpHandler {
    public void handle(HttpExchange httpExchange) throws IOException {
      String sentence = httpExchange.getRequestURI().getQuery();

      System.out.print("GET:/name ... ");
      System.out.println(sentence);

      Segment segment = HanLP.newSegment().enableNameRecognize(true);
      List<Term> termList = segment.seg(sentence);

      String names = termList.stream()
          .filter(term -> term.nature == Nature.fromString("nr"))
          .map(term -> term.word)
          .collect(Collectors.joining(","));

      byte[] response = names.getBytes();
      httpExchange.sendResponseHeaders(200, response.length);

      OutputStream os = httpExchange.getResponseBody();
      os.write(response);
      os.close();
    }
  }
}
