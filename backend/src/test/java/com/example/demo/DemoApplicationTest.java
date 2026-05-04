package com.example.demo;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DemoApplicationTest {

    @Test
    void testApplicationInstantiation() {
        DemoApplication app = new DemoApplication();
        assertNotNull(app);
    }

    @Test
    void testMainMethod() {
        assertDoesNotThrow(() -> {
            DemoApplication.main(new String[]{});
        });
    }
}
