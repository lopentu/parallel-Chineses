package ntu.ltcl.hanlp;

import java.io.IOException;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpServer;

public class HanLPhttp {

  public static void main(String[] args) throws Exception {
    HttpServer server = HttpServer.create(new InetSocketAddress(5217), 0);

    server.createContext("/test", new TestHandler());
    server.createContext("/test/", new TestHandler());

    server.createContext("/name", new NameHandler());
    server.createContext("/name/", new NameHandler());

    server.createContext("/translated_name", new TranslatedNameHandler());
    server.createContext("/translated_name/", new TranslatedNameHandler());

    server.setExecutor(null);

    server.start();
  }

}
