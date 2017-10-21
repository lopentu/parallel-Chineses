package ntu.ltcl.hanlp;

import java.io.IOException;

import java.util.List;
import java.util.Map;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.hankcs.hanlp.corpus.tag.Nature;

public class TestHandler extends Handler {
  public void handle(HttpExchange httpExchange) throws IOException {
    System.out.println("GET:/test");

    writeResponse(httpExchange, "It works.");
  }
}
