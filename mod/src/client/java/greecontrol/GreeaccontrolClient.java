package greecontrol;

import greecontrol.event.GameTickHandler;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.RunArgs;

import java.net.http.HttpClient;

public class GreeaccontrolClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		HttpClient http_client = HttpClient.newHttpClient();
		GameTickHandler tick_handler = new GameTickHandler();
		// This entrypoint is suitable for setting up client-specific logic, such as rendering.
		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			if (MinecraftClient.getInstance().player != null) {
				tick_handler.onTick(MinecraftClient.getInstance().player, http_client);
			}
		});
	}
}
