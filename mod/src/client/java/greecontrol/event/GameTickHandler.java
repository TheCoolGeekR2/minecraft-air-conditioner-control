package greecontrol.event;

import com.google.gson.JsonObject;
import net.minecraft.registry.entry.RegistryEntry;
import net.minecraft.world.World;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.biome.Biome;
import net.minecraft.client.network.ClientPlayerEntity;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.net.http.HttpRequest.BodyPublishers;

import net.minecraft.registry.RegistryKey;
import net.minecraft.util.Identifier;

enum TimeOfDay{
    DAY,
    NIGHT
}

public class GameTickHandler {
    String AC_API = "http://127.0.0.1:8080/biome";
    RegistryEntry<Biome> CurrentPlayerBiome = null;
    TimeOfDay CurrentTimeOfDay = null;
    static long DAY_START = 0;
    static long DAY_END = 12000;

    private TimeOfDay GetTimeOfDay(ClientPlayerEntity player) {
        World world = player.getEntityWorld();
        long time = world.getTimeOfDay();

        if(DAY_END > time && time > DAY_START) {
            return TimeOfDay.DAY;
        }
        else return TimeOfDay.NIGHT;
    }

    private RegistryEntry<Biome> GetPlayerBiome(ClientPlayerEntity player) {
        BlockPos pos = player.getBlockPos();
        World world = player.getEntityWorld();
        return world.getBiome(pos);
    }
    private static Identifier getClientBiomeId(RegistryEntry<Biome> biomeEntry) {
        return biomeEntry.getKey()
                .map(RegistryKey::getValue)
                .orElse(null); // or handle however you like
    }

    private void sendBiome(HttpClient client, Identifier BiomeID) {
        String biome_parameter = "{ \"biome\": \"" + BiomeID.toString() + "\" }";
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(AC_API))
                .POST(BodyPublishers.ofString(biome_parameter))
                .build();
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString());
    }

    private void sendParameter(HttpClient client, String key, String value) {
        JsonObject parameters = new JsonObject();
        parameters.addProperty(key, value);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(AC_API))
                .POST(BodyPublishers.ofString(parameters.toString()))
                .build();
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString());
    }

        private boolean shouldSendBiome(RegistryEntry<Biome> NewBiome) {
        return NewBiome != CurrentPlayerBiome;
    }

    private boolean shouldSendTimeOfDay(TimeOfDay NewTimeOfDay) {
        return NewTimeOfDay != CurrentTimeOfDay;
    }

    public void onTick(ClientPlayerEntity player, HttpClient client) {
        RegistryEntry<Biome> biome = GetPlayerBiome(player);
        TimeOfDay TimeOfDay = GetTimeOfDay(player);
        if (shouldSendBiome(biome)) {
            CurrentPlayerBiome = biome;
            sendBiome(client, getClientBiomeId(CurrentPlayerBiome));
        }
        if (shouldSendTimeOfDay(TimeOfDay)) {
            CurrentTimeOfDay = TimeOfDay;

        }
    }
}